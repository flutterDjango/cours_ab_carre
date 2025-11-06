from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
from wagtail.models import Site
from .forms import ContactForm
from .models import ContactSettings


def contact_view(request):
    # Récupérer les settings Wagtail pour le site actuel
    current_site = Site.find_for_request(request)
    if current_site is None:
        current_site = Site.objects.get(is_default_site=True)
    site_settings = ContactSettings.for_site(current_site)

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            # Valeurs Wagtail Settings
            admin_subject = site_settings.get_email_subject()
            admin_to = [site_settings.get_to_address()]

            confirmation_subject = f"Merci pour votre message, {name}"
            confirmation_body = (
                f"Bonjour {name},\n\nMerci pour votre message !\n\n"
                f"Votre message:\n{message}\n\n"
                "Nous vous répondrons dans les plus brefs délais."
            )

            # Connexion SMTP OVH
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

            # Email admin
            EmailMessage(
                subject=admin_subject,
                body=f"Message depuis la page Contact\n\nNom: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.CONTACT_FROM_EMAIL,
                to=admin_to,
                connection=conn,
            ).send()

            # Email de confirmation utilisateur
            if email:
                EmailMessage(
                    subject=confirmation_subject,
                    body=confirmation_body,
                    from_email=settings.CONTACT_FROM_EMAIL,
                    to=[email],
                    connection=conn,
                ).send()

            # Redirection vers la page "merci"
            return redirect(reverse("contact:contact_thank_you"))

    else:
        form = ContactForm()

    return render(request, "contact/contact_page.html", {"form": form})


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
