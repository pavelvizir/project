# Generated by Django 2.0.3 on 2018-03-31 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180313_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PID', models.IntegerField()),
                ('CID', models.IntegerField()),
                ('Psource', models.CharField(max_length=100)),
                ('Csource', models.CharField(max_length=500)),
                ('Type', models.CharField(max_length=100)),
                ('Metadata', models.TextField()),
                ('Data_main', models.TextField()),
                ('Additional_data', models.TextField()),
                ('Link', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Data_providers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Provider', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=100)),
                ('Type', models.CharField(max_length=100)),
                ('Last_number', models.IntegerField()),
            ],
        ),
    ]