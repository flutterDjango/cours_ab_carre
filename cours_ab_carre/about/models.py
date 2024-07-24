from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class AboutPage(Page):
    about_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('about_text')
        ]
