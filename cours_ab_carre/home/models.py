
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from ..streams import blocks
# from .blocks import BodyBlock


class HomePage(Page):

    template = "home/home_page.html"
    max_count = 1
    text = StreamField(
        [
            ("text", blocks.RichtextBlock()),
        ],
        blank=True,
        null=True,
        block_counts={
            'text': {'min_num': 1},
        })
    # questions = StreamField(
    #     [
    #         ("text", blocks.RichtextBlock()),
    #     ],
    #     blank=True,
    #     null=True,
    #     block_counts={
    #         'text': {'min_num': 1, 'max_num': 4},
    #     }
    # )
    testimonials = StreamField(
        [
            ("testimonials", blocks.TitleAndTextBlock()),
        ],
        blank=True,
        null=True,
        )

    questions_content = StreamField(
        [
            ("markdown_question", blocks.MarkdownBlock()),
        ],
        blank=True,
        null=True,
        block_counts={
            "markdown_question": {'min_num': 1, 'max_num': 4},
            }
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('questions_content'),
                FieldPanel('text'),
                FieldPanel('testimonials')
            ],
            heading="Body",
        ),
    ]
