# Generated by Django 2.2.12 on 2021-09-10 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='add_watchlist',
        ),
    ]