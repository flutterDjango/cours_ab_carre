# Generated by Django 5.0.7 on 2024-07-23 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_contactpage_gdpr_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactpage',
            name='gdpr_box',
        ),
        migrations.RemoveField(
            model_name='contactpage',
            name='gdpr_text',
        ),
    ]
