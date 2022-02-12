# Generated by Django 3.2.12 on 2022-02-11 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0009_auto_20220212_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='report_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
