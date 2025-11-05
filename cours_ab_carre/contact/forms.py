# contact/forms.py
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Votre nom"}),
    )
    email = forms.EmailField(
        label="Adresse email",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "votre@email.com"}),
    )
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Votre message", "rows": 6}
        ),
    )

    # ReCAPTCHA — utilise V2 checkbox par défaut ; adapte le widget si tu
    # veux v3
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Veuillez indiquer votre nom.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 5:
            raise forms.ValidationError("Le message est trop court.")
        return message
