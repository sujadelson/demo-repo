# Generated by Django 3.0.8 on 2021-10-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusBookingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('bus', models.CharField(max_length=30)),
                ('source', models.CharField(max_length=30)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival', models.CharField(max_length=30)),
                ('arrival_date', models.DateField()),
                ('arrival_time', models.TimeField()),
                ('bus_type', models.CharField(max_length=30)),
                ('no_of_seat', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
