# Generated by Django 4.0.5 on 2022-07-09 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LinkedinApp', '0003_alter_linkedin_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedin_profils',
            name='certifications',
            field=models.CharField(blank=True, default='NaN', max_length=200),
        ),
        migrations.AddField(
            model_name='linkedin_profils',
            name='sector',
            field=models.CharField(blank=True, default='NaN', max_length=200),
        ),
    ]