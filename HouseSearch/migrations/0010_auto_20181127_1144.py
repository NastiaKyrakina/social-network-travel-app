# Generated by Django 2.1.2 on 2018-11-27 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('HouseSearch', '0009_auto_20181123_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
