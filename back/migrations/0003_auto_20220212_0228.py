# Generated by Django 3.2.12 on 2022-02-11 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('back', '0002_auto_20210328_0302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.TextField()),
                ('website', models.URLField()),
                ('report_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('text', models.TextField()),
                ('location', models.TextField(blank=True, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=11, max_digits=14, null=True)),
                ('time_of_incident', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('sent', 'Отправлено'), ('verified', 'Подтверждено'), ('canceled', 'Отмена')], default='sent', max_length=15)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SignalProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('group', models.CharField(choices=[('smells', 'Запахи'), ('symptoms', 'Симптомы')], default='smells', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='SignalToInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('text', models.TextField()),
                ('time_of_report', models.DateTimeField(auto_now=True)),
                ('response', models.TextField()),
                ('time_of_response', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('in_processing', 'В обработке'), ('ignore', 'Не дали ответ'), ('answered', 'Ответили'), ('failed_to_call', 'Не удалось дозвониться'), ('other', 'Другое')], default='in_processing', max_length=15)),
                ('other_comment', models.TextField()),
                ('instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='back.instance')),
                ('signal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='back.signal')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='sensor',
            name='public',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.CreateModel(
            name='SignalToInstanceMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('file', models.FileField(upload_to='')),
                ('signal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media', to='back.signaltoinstance')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SignalMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('file', models.FileField(upload_to='')),
                ('signal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media', to='back.signal')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='signal',
            name='properties',
            field=models.ManyToManyField(related_name='reports', to='back.SignalProperties'),
        ),
    ]
