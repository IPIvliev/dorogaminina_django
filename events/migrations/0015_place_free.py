# Generated by Django 4.0.4 on 2022-06-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_place_busy'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='free',
            field=models.IntegerField(default=0),
        ),
    ]