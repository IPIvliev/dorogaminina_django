# Generated by Django 4.0.4 on 2022-06-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_alter_order_order_place_merch_order_order_merch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merch',
            name='merch_image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/merchs/'),
        ),
    ]
