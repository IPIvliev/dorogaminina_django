# Generated by Django 4.0.4 on 2022-06-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.IntegerField(default=0, max_length=5),
        ),
    ]
