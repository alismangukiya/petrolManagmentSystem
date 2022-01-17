# Generated by Django 4.0 on 2022-01-12 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0006_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuelname', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('sellPrice', models.IntegerField()),
                ('buyingPrice', models.IntegerField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyname', models.CharField(max_length=255)),
                ('branchcode', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', to_field='username')),
            ],
        ),
    ]
