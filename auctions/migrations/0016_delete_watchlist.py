# Generated by Django 2.2.12 on 2021-09-10 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_watchlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
