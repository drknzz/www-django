# Generated by Django 3.2 on 2021-04-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='file',
            name='availability',
            field=models.BooleanField(default=True),
        ),
    ]
