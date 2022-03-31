# Generated by Django 2.2.8 on 2020-02-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0006_auto_20191215_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlecalendar',
            name='google_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='googlemaps',
            name='google_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='index',
            name='google_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='google_ad_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
