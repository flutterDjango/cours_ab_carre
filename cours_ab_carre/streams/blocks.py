from wagtail import blocks
from wagtailmarkdown.blocks import MarkdownBlock


class RichtextBlock(blocks.RichTextBlock):
    """Richtext avec toutes les caractèristiques"""
    
    class Meta:
        template = "streams/text_block.html"
        icon = "edit"
        label = "Full RichText"
        

# from wagtail.images.blocks import ImageChooserBlock
# from wagtailcodeblock.blocks import CodeBlock


class MarkdownBlock(blocks.StreamBlock):
    markdown = MarkdownBlock(icon="code")

    class Meta:
        # template = "streams/text_block.html"
        icon = "edit"
        label = "Markdown Language"


class TitleAndTextBlock(blocks.StructBlock):
    """Titre et texte."""

    title = blocks.CharBlock(required=True, help_text='Ajouter un titre')
    text = blocks.TextBlock(required=True, help_text='Ajouter un texte')

    class Meta:
        template = "streams/card_title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
