# Generated by Django 5.0.4 on 2024-06-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sequrity', '0005_ownerprofile_registration_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
