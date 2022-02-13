# Generated by Django 3.2.12 on 2022-02-11 23:25

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0005_auto_20220212_0353'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.TextField()),
                ('website', models.URLField()),
                ('location', models.TextField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('danger_score', models.FloatField(default=0, max_length=1)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factory', to='back.city')),
                ('factory_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factory', to='back.factorytype')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
