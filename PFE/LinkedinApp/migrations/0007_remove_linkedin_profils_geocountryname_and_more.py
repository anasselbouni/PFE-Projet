# Generated by Django 4.0.5 on 2022-08-06 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LinkedinApp', '0006_rename_sector_linkedin_profils_industryname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkedin_profils',
            name='geoCountryName',
        ),
        migrations.RemoveField(
            model_name='linkedin_profils',
            name='geoLocationName',
        ),
    ]
