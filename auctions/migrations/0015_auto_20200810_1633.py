# Generated by Django 3.0.8 on 2020-08-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_remove_watch_list_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='img',
            field=models.ImageField(blank=True, default='images/default_img.png', null=True, upload_to=''),
        ),
    ]
