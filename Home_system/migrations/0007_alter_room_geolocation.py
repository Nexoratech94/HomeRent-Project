# Generated by Django 5.0.4 on 2024-06-08 11:03

import django_google_maps.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home_system', '0006_room_geolocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(default='0,0', max_length=100),
        ),
    ]
