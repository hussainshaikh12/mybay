# Generated by Django 3.0.8 on 2020-08-20 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20200820_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='sold_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
