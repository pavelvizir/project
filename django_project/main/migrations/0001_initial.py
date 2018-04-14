from django.db import migrations, models
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PID', models.IntegerField()),
                ('CID', models.IntegerField()),
                ('psource', models.CharField(max_length=100)),
                ('csource', models.CharField(max_length=500)),
                ('type', models.CharField(max_length=100)),
                ('metadata', models.TextField()),
                ('data_main', models.TextField()),
                ('additional_data', models.TextField()),
                ('link', models.CharField(max_length=500)),
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

