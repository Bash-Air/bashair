# Generated by Django 3.2.12 on 2022-02-11 22:52

import autoslug.fields
import cities_light.abstract_models
import cities_light.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0003_auto_20220212_0228'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(blank=True, db_index=True, default='', max_length=4000)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('population', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('feature_code', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('timezone', models.CharField(blank=True, db_index=True, max_length=40, null=True, validators=[cities_light.validators.timezone_validator])),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('code2', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('code3', models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ('continent', models.CharField(choices=[('OC', 'Oceania'), ('EU', 'Europe'), ('AF', 'Africa'), ('NA', 'North America'), ('AN', 'Antarctica'), ('SA', 'South America'), ('AS', 'Asia')], db_index=True, max_length=2)),
                ('tld', models.CharField(blank=True, db_index=True, max_length=5)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'region/state',
                'verbose_name_plural': 'regions/states',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'SubRegion',
                'verbose_name_plural': 'SubRegions',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveIndex(
            model_name='sensorlocation',
            name='country_idx',
        ),
        migrations.RemoveIndex(
            model_name='sensorlocation',
            name='city_idx',
        ),
        migrations.RenameField(
            model_name='sensorlocation',
            old_name='city',
            new_name='city_old',
        ),
        migrations.RemoveField(
            model_name='sensorlocation',
            name='country',
        ),
        migrations.AddField(
            model_name='subregion',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.country'),
        ),
        migrations.AddField(
            model_name='subregion',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back.region'),
        ),
        migrations.AddField(
            model_name='region',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.country'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.country'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back.region'),
        ),
        migrations.AddField(
            model_name='city',
            name='subregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='back.subregion'),
        ),
        migrations.AddField(
            model_name='instance',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instance', to='back.city'),
        ),
        migrations.AddField(
            model_name='signal',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signal', to='back.city'),
        ),
        migrations.AlterUniqueTogether(
            name='region',
            unique_together={('country', 'slug'), ('country', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('region', 'subregion', 'slug'), ('region', 'subregion', 'name')},
        ),
    ]
