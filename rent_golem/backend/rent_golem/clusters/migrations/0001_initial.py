# Generated by Django 4.2.4 on 2023-08-25 13:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('package', models.CharField(choices=[('automatic', 'Automatic')], max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('shutting-down', 'Shutting Down'), ('terminated', 'Terminated')], default='pending', max_length=255)),
                ('additional_params', models.JSONField()),
                ('size', models.PositiveIntegerField(help_text='Number of desired workers.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('address', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('runpod', 'Runpod')], max_length=255)),
                ('service_id', models.CharField(help_text='ID of worker in provider space.', max_length=255, null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
                ('status', models.CharField(choices=[('starting', 'Starting'), ('ok', 'Ok'), ('bad', 'Bad'), ('stopped', 'Stopped')], default='starting', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('cluster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='clusters.cluster')),
            ],
        ),
    ]
