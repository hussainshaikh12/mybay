# Generated by Django 3.0.8 on 2020-08-08 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200808_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='sold_on',
            field=models.DateField(blank=True, default=None),
        ),
    ]
