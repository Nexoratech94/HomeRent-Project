# Generated by Django 5.0.4 on 2024-06-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_system', '0014_alter_room_geolocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='geolocation',
            field=models.CharField(default='0.0,0.0', max_length=100),
        ),
    ]
