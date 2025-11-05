# contact/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import get_connection, EmailMessage
from .forms import ContactForm  # ton formulaire Django avec ReCAPTCHA intégré


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupération des données utilisateur
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            # Contenu pour l'email admin
            admin_subject = settings.CONTACT_EMAIL_SUBJECT
            admin_body = f"Message depuis la page Contact\n\nNom: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Contenu pour l'email utilisateur
            confirmation_subject = f"Merci pour votre message, {name}"
            confirmation_body = (
                f"Bonjour {name},\n\nMerci pour votre message !\n\n"
                f"Votre message:\n{message}\n\n"
                "Nous vous répondrons dans les plus brefs délais."
            )

            # Ouverture d'une connexion SMTP OVH
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

            # Envoi email admin
            admin_email = EmailMessage(
                subject=admin_subject,
                body=admin_body,
                from_email=settings.CONTACT_FROM_EMAIL,
                to=[settings.CONTACT_TO_EMAIL],
                connection=conn,
            )
            admin_email.send()

            # Envoi email confirmation à l'utilisateur
            if email:
                user_email_msg = EmailMessage(
                    subject=confirmation_subject,
                    body=confirmation_body,
                    from_email=settings.CONTACT_FROM_EMAIL,
                    to=[email],
                    connection=conn,
                )
                user_email_msg.send()

            # Redirection vers la page "merci"
            return redirect(reverse("contact:contact_thank_you"))

    else:
        form = ContactForm()

    return render(request, "contact/contact_page.html", {"form": form})
