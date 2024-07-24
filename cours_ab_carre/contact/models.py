from django.db import models
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.admin.panels import (FieldPanel,
                                  FieldRowPanel,
                                  MultiFieldPanel,
                                  InlinePanel)
from modelcluster.fields import ParentalKey
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage',
                       on_delete=models.CASCADE,
                       related_name='form_fields')


class ContactPage(WagtailCaptchaEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"
    body = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('body'),
        InlinePanel('form_fields', label='Custom Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('from_address'),
                    FieldPanel('to_address'),
                ]),
                FieldPanel('subject'),
            ], heading="Email Settings"
        )
    ]
# https://www.youtube.com/watch?v=kAblCAxsWzY&list=PLMQHMcNi6ocsS8Bfnuy_IDgJ4bHRRrvub&index=30

# https://www.youtube.com/watch?v=-MS6E_pHOfI&list=PLMQHMcNi6ocsS8Bfnuy_IDgJ4bHRRrvub&index=31