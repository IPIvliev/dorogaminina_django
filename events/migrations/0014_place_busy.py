# Generated by Django 4.0.4 on 2022-06-06 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_event_id_alter_merch_id_alter_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='busy',
            field=models.IntegerField(default=0),
        ),
    ]