# Generated by Django 4.0.4 on 2022-06-09 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_email_event_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон мероприятия'),
        ),
    ]
