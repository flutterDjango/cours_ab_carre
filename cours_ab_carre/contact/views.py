from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from wagtail.models import Site

from .blacklist_models import BlacklistedEmail, BlacklistedName
from .forms import ContactForm
from .models import ContactSettings


def normalize(value: str) -> str:
    return value.strip().lower()


def contact_view(request):
    # Récupérer le site Wagtail courant
    current_site = Site.find_for_request(request)
    if current_site is None:
        current_site = Site.objects.get(is_default_site=True)

    site_settings = ContactSettings.for_site(current_site)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = normalize(form.cleaned_data.get("name", ""))
            email = normalize(form.cleaned_data.get("email", ""))
            message = form.cleaned_data.get("message")

            # Valeurs Wagtail Settings
            admin_subject = site_settings.get_email_subject()
            admin_to = [site_settings.get_to_address()]

            # Email de confirmation utilisateur
            confirmation_subject = f"Merci pour votre message, {name}"
            confirmation_body = (
                "Ceci est un message automatique, "
                "merci de ne pas répondre.\n\n"
                f"Bonjour {name},\n\n"
                "Merci pour votre message !\n\n"
                f"Votre message:\n{message}\n\n"
                "Nous vous répondrons dans les plus brefs délais."
            )

            # Connexion SMTP
            conn = get_connection(
                backend="django.core.mail.backends.smtp.EmailBackend",
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
                use_ssl=settings.EMAIL_USE_SSL,
                fail_silently=False,
            )
            conn.open()

            # ----------------------------
            # Vérification blacklist
            # ----------------------------
            blacklisted = False

            # Vérification par email
            if email:
                try:
                    bl_email = BlacklistedEmail.objects.get(email=email)
                    bl_email.attempt_count += 1
                    bl_email.last_attempt_at = timezone.now()
                    bl_email.save(
                        update_fields=["attempt_count", "last_attempt_at"]
                    )
                    blacklisted = True
                except BlacklistedEmail.DoesNotExist:
                    pass

            # Vérification par nom (si pas déjà blacklisté)
            if not blacklisted and name:
                try:
                    bl_name = BlacklistedName.objects.get(name=name)
                    bl_name.attempt_count += 1
                    bl_name.last_attempt_at = timezone.now()
                    bl_name.save(
                        update_fields=["attempt_count", "last_attempt_at"]
                    )
                    blacklisted = True
                except BlacklistedName.DoesNotExist:
                    pass

            # ----------------------------
            # Envoi email admin
            # ----------------------------
            if not blacklisted:
                EmailMessage(
                    subject=admin_subject,
                    body=(
                        "Message depuis la page Contact\n\n"
                        f"Nom: {name}\n"
                        f"Email: {email}\n\n"
                        f"Message:\n{message}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    to=admin_to,
                    connection=conn,
                ).send()

            # ----------------------------
            # Email de confirmation utilisateur (TOUJOURS)
            # ----------------------------
            if email:
                EmailMessage(
                    subject=confirmation_subject,
                    body=confirmation_body,
                    from_email=settings.CONTACT_FROM_EMAIL,
                    to=[email],
                    headers={
                        "Reply-To": settings.CONTACT_FROM_EMAIL,
                        "Auto-Submitted": "auto-generated",
                    },
                    connection=conn,
                ).send()

            # Redirection vers la page "merci"
            return redirect(reverse("contact:contact_thank_you"))

    else:
        form = ContactForm()

    return render(
        request,
        "contact/contact_page.html",
        {"form": form},
    )


def thank_you_view(request):
    current_site = Site.find_for_request(request) or Site.objects.get(
        is_default_site=True
    )
    site_settings = ContactSettings.for_site(current_site)
    return render(
        request,
        "contact/contact_page_landing.html",
        {"thank_you_text": site_settings.thank_you_text},
    )
