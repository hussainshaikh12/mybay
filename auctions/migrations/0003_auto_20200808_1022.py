# Generated by Django 3.0.8 on 2020-08-08 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing_bids_comments_watch_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='category',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='img',
            field=models.ImageField(blank=True, default='', upload_to='al_images'),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
