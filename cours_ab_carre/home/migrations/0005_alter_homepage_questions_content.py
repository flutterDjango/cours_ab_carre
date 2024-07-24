# Generated by Django 5.0.7 on 2024-07-19 08:18

import wagtail.blocks
import wagtail.fields
import wagtailmarkdown.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_homepage_questions_homepage_questions_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='questions_content',
            field=wagtail.fields.StreamField([('markdown_question', wagtail.blocks.StreamBlock([('markdown', wagtailmarkdown.blocks.MarkdownBlock(icon='code'))]))], blank=True, null=True),
        ),
    ]
