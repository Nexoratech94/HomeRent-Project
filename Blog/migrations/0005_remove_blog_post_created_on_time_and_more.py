# Generated by Django 5.0.4 on 2024-04-29 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_blog_post_author_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog_post',
            name='created_on_time',
        ),
        migrations.RemoveField(
            model_name='blog_post',
            name='slug',
        ),
        migrations.AlterField(
            model_name='blog_post',
            name='created_on_date',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
