# Generated by Django 3.2.12 on 2022-02-18 21:28

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0023_auto_20220219_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='factory',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326, verbose_name='Периметр территория'),
        ),
    ]