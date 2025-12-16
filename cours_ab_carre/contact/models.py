# contact/models.py
from django.db import models
from django.conf import settings

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from wagtail.fields import RichTextField
from .blacklist_models import BlacklistedEmail, BlacklistedName  # noqa


@register_setting
class ContactSettings(BaseSiteSetting):
    """
    Réglages éditables pour la page Contact (adresse destinataire, sujet,
    texte merci).
    Valeurs par défaut prises depuis les variables d'environnement / settings.
    """

    to_address = models.EmailField(
        blank=True,
        help_text="Adresse qui recevra les messages du formulaire. Si vide,"
        "on utilisera settings.CONTACT_TO_EMAIL.",
        default=getattr(settings, "CONTACT_TO_EMAIL", ""),
    )

    email_subject = models.CharField(
        max_length=255,
        blank=True,
        help_text="Objet du mail envoyé à l’administrateur. Si vide,"
        "on utilisera settings.CONTACT_EMAIL_SUBJECT.",
        default=getattr(
            settings,
            "CONTACT_EMAIL_SUBJECT",
            "Nouveau message depuis le formulaire de contact",
        ),
    )

    thank_you_text = RichTextField(
        blank=True,
        help_text="Texte affiché sur la page de remerciement (HTML autorisé).",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("email_subject"),
            ],
            heading="Paramètres d'envoi d'email",
        ),
        FieldPanel("thank_you_text"),
    ]

    def get_to_address(self):
        return self.to_address or getattr(settings, "CONTACT_TO_EMAIL", "")

    def get_email_subject(self):
        return self.email_subject or getattr(
            settings, "CONTACT_EMAIL_SUBJECT", ""
        )
