# Generated by Django 3.0.8 on 2020-08-14 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200809_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
