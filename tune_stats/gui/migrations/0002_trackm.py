# Generated by Django 4.1.5 on 2023-02-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('artist_id', models.CharField(max_length=150)),
                ('track_id', models.CharField(max_length=150)),
                ('image', models.CharField(max_length=150)),
                ('album_name', models.CharField(max_length=150)),
            ],
        ),
    ]
