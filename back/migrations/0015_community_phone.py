# Generated by Django 3.2.12 on 2022-02-12 02:47

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0014_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]