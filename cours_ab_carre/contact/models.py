from django.db import models
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    InlinePanel,
)
from modelcluster.fields import ParentalKey
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from django.conf import settings
from django.core.mail import send_mail
# from django.template.loader import render_to_string


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(WagtailCaptchaEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"

    body = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    to_address = models.EmailField(
        blank=True,
        default=settings.CONTACT_TO_EMAIL,
        help_text=f"Adresse qui recevra les messages du formulaire. "
        f"Par défaut : {settings.CONTACT_TO_EMAIL}",
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text=f"Objet du mail envoyé à l’administrateur. "
        f"Par défaut : « {settings.CONTACT_EMAIL_SUBJECT} »",
    )

    # ✉️ Nouveau : email de confirmation
    confirmation_subject = models.CharField(
        max_length=255,
        blank=True,
        default="Merci pour votre message",
        help_text="Objet de l’email de confirmation envoyé au visiteur.",
    )

    confirmation_message = RichTextField(
        blank=True,
        help_text="Texte du mail de confirmation (vous pouvez inclure une "
        "formule de politesse). "
        "Le message de l’utilisateur sera ajouté automatiquement à la fin.",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("body"),
        InlinePanel("form_fields", label="Champs personnalisés"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
                FieldPanel("confirmation_subject"),
                FieldPanel("confirmation_message"),
            ],
            heading="Paramètres d'envoi d'email",
        ),
    ]

    def get_to_address(self):
        return self.to_address or settings.CONTACT_TO_EMAIL

    def get_subject(self):
        return self.subject or settings.CONTACT_EMAIL_SUBJECT

    def process_form_submission(self, form):
        """Envoie l'email principal + confirmation au visiteur."""
        super().process_form_submission(form)

        # Récupère l’adresse de l’utilisateur
        user_email = form.cleaned_data.get(
            "email"
        )  # supposant que ton champ du formulaire s'appelle "email"
        user_message = form.cleaned_data.get("message", "")

        if user_email:
            confirmation_subject = (
                self.confirmation_subject or "Merci pour votre message"
            )
            confirmation_body = f"{self.confirmation_message}\n\n---\n"
            f"Voici le message que vous avez envoyé :\n\n{user_message}"

            try:
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email=settings.CONTACT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                    # on ne bloque pas la soumission du formulaire
                )
            except Exception:
                # Optionnel : loguer l’erreur sans perturber l’utilisateur
                pass


# https://www.youtube.com/watch?v=kAblCAxsWzY&list=PLMQHMcNi6ocsS8Bfnuy_IDgJ4bHRRrvub&index=30

# https://www.youtube.com/watch?v=-MS6E_pHOfI&list=PLMQHMcNi6ocsS8Bfnuy_IDgJ4bHRRrvub&index=31
