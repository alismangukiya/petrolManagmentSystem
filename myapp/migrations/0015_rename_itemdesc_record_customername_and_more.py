# Generated by Django 4.0 on 2022-01-17 04:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='itemDesc',
            new_name='customername',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='itemName',
            new_name='fuelname',
        ),
        migrations.RemoveField(
            model_name='record',
            name='customerName',
        ),
        migrations.RemoveField(
            model_name='record',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='record',
            name='username',
        ),
        migrations.AddField(
            model_name='record',
            name='phonenumber',
            field=models.IntegerField(default='NULL'),
        ),
        migrations.AddField(
            model_name='record',
            name='platenumber',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='fuel',
            name='date',
            field=models.DateField(default=datetime.date(2022, 1, 17)),
        ),
    ]
