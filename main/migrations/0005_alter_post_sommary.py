# Generated by Django 5.0.6 on 2024-06-26 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_post_sommary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sommary',
            field=models.CharField(max_length=250, verbose_name='Sommary'),
        ),
    ]
