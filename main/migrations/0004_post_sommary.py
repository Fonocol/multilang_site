# Generated by Django 5.0.6 on 2024-06-26 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_post_options_alter_post_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sommary',
            field=models.CharField(default="draft aui c'ets cool", max_length=250, verbose_name='Sommary'),
        ),
    ]
