# Generated by Django 3.2.12 on 2022-02-19 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0026_auto_20220219_0447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factory',
            name='address',
        ),
        migrations.RemoveField(
            model_name='node',
            name='last_notify',
        ),
    ]
