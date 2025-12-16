# contact/blacklist_models.py
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class BlacklistedEmail(models.Model):
    email = models.EmailField(
        unique=True,
        help_text="Adresse email blacklistée (insensible à la casse).",
    )

    attempt_count = models.PositiveIntegerField(
        default=0, help_text="Nombre de tentatives bloquées."
    )

    last_attempt_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date et heure de la dernière tentative.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date d’ajout à la blacklist."
    )

    panels = [
        FieldPanel("email"),
        FieldPanel("attempt_count", read_only=True),
        FieldPanel("last_attempt_at", read_only=True),
        FieldPanel("created_at", read_only=True),
    ]

    class Meta:
        verbose_name = "Email blacklisté"
        verbose_name_plural = "Emails blacklistés"
        ordering = ["-last_attempt_at"]

    def __str__(self):
        return self.email.lower()


@register_snippet
class BlacklistedName(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="Nom blacklisté (insensible à la casse).",
    )

    attempt_count = models.PositiveIntegerField(
        default=0, help_text="Nombre de tentatives bloquées."
    )

    last_attempt_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date et heure de la dernière tentative.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date d’ajout à la blacklist."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("attempt_count", read_only=True),
        FieldPanel("last_attempt_at", read_only=True),
        FieldPanel("created_at", read_only=True),
    ]

    class Meta:
        verbose_name = "Nom blacklisté"
        verbose_name_plural = "Noms blacklistés"
        ordering = ["-last_attempt_at"]

    def __str__(self):
        return self.name.lower()
