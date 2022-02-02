# Generated by Django 3.1.7 on 2021-03-27 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uid', models.SlugField(unique=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('height', models.IntegerField(null=True)),
                ('sensor_position', models.IntegerField(null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('last_notify', models.DateTimeField(blank=True, null=True)),
                ('description_internal', models.TextField(blank=True, null=True)),
                ('indoor', models.BooleanField(default=False)),
                ('inactive', models.BooleanField(default=False)),
                ('exact_location', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['uid'],
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('pin', models.CharField(db_index=True, default='-', help_text='differentiate the sensors on one node by giving pin used', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('public', models.BooleanField(db_index=True, default=False)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensors', to='back.node')),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('sampling_rate', models.IntegerField(blank=True, help_text='in milliseconds', null=True)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('software_version', models.CharField(default='', help_text='sensor software version', max_length=100)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uid', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('manufacturer', models.CharField(max_length=1000)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('location', models.TextField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('altitude', models.DecimalField(blank=True, decimal_places=8, max_digits=14, null=True)),
                ('indoor', models.BooleanField(default=False)),
                ('street_name', models.TextField(blank=True, null=True)),
                ('street_number', models.TextField(blank=True, null=True)),
                ('postalcode', models.TextField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('traffic_in_area', models.IntegerField(null=True)),
                ('oven_in_area', models.IntegerField(null=True)),
                ('industry_in_area', models.IntegerField(null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(blank=True, help_text='If not set, location is public.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['location'],
            },
        ),
        migrations.CreateModel(
            name='SensorDataValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.TextField()),
                ('value_type', models.CharField(choices=[('P0', '1µm particles'), ('P1', '10µm particles'), ('P2', '2.5µm particles'), ('durP1', 'duration 1µm'), ('durP2', 'duration 2.5µm'), ('ratioP1', 'ratio 1µm in percent'), ('ratioP2', 'ratio 2.5µm in percent'), ('samples', 'samples'), ('min_micro', 'min_micro'), ('max_micro', 'max_micro'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('pressure', 'Pa'), ('altitude', 'meter'), ('pressure_sealevel', 'Pa (sealevel)'), ('brightness', 'Brightness'), ('dust_density', 'Dust density in mg/m3'), ('vo_raw', 'Dust voltage raw'), ('voltage', 'Dust voltage calculated'), ('P10', '1µm particles'), ('P25', '2.5µm particles'), ('durP10', 'duration 1µm'), ('durP25', 'duration 2.5µm'), ('ratioP10', 'ratio 1µm in percent'), ('ratioP25', 'ratio 2.5µm in percent'), ('door_state', 'door state (open/closed)'), ('lat', 'latitude'), ('lon', 'longitude'), ('height', 'height'), ('hdop', 'horizontal dilusion of precision'), ('timestamp', 'measured timestamp'), ('age', 'measured age'), ('satelites', 'number of satelites'), ('speed', 'current speed over ground'), ('azimuth', 'track angle'), ('noise_L01', 'Sound level L01'), ('noise_L95', 'Sound level L95'), ('noise_Leq', 'Sound level Leq'), ('co_kohm', 'CO in kOhm'), ('co_ppb', 'CO in ppb'), ('eco2', 'eCO2 in ppm'), ('no2_kohm', 'NO2 in kOhm'), ('no2_ppb', 'NO2 in ppb'), ('ozone_ppb', 'O3 in ppb'), ('so2_ppb', 'SO2 in ppb')], db_index=True, max_length=100)),
                ('sensordata', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensordatavalues', to='back.sensordata')),
            ],
        ),
        migrations.AddField(
            model_name='sensordata',
            name='location',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back.sensorlocation'),
        ),
        migrations.AddField(
            model_name='sensordata',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sensordatas', to='back.sensor'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='back.sensortype'),
        ),
        migrations.AddField(
            model_name='node',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='back.sensorlocation'),
        ),
        migrations.AddField(
            model_name='node',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='sensorlocation',
            index=models.Index(fields=['country'], name='country_idx'),
        ),
        migrations.AddIndex(
            model_name='sensorlocation',
            index=models.Index(fields=['city'], name='city_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='sensordatavalue',
            unique_together={('sensordata', 'value_type')},
        ),
        migrations.AlterIndexTogether(
            name='sensordata',
            index_together={('modified',)},
        ),
        migrations.AlterUniqueTogether(
            name='sensor',
            unique_together={('node', 'pin')},
        ),
    ]