# Generated by Django 3.2.12 on 2022-02-12 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0015_community_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='email',
        ),
    ]
