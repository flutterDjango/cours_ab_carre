from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class LegalNoticePage(Page):
    legal_notice_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('legal_notice_text')
        ]


class CGUPage(Page):
    cgu_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('cgu_text')
        ]


class GDPRPage(Page):
    gdpr_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('gdpr_text')
        ]


class CookiesPage(Page):
    cookies_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('cookies_text')
        ]
