# Generated by Django 3.0.8 on 2020-08-16 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20200816_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='bidders_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='watchers_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]