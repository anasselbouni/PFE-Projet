# Generated by Django 4.0.5 on 2022-07-09 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LinkedinApp', '0005_linkedin_profils_education_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkedin_profils',
            old_name='sector',
            new_name='industryName',
        ),
    ]
