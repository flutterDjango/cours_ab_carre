# Generated by Django 5.0.6 on 2024-07-03 16:00

import cours_ab_carre.streams.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='questions',
            field=wagtail.fields.StreamField([('text', cours_ab_carre.streams.blocks.RichtextBlock())], blank=True, null=True),
        ),
    ]
