# Generated by Django 3.2.12 on 2022-02-12 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0011_alter_instance_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factory',
            name='phone',
        ),
    ]
