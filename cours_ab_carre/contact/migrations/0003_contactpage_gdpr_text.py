# Generated by Django 5.0.7 on 2024-07-23 09:17

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_contactpage_gdpr_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='gdpr_text',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
