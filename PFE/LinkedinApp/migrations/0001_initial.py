# Generated by Django 4.0.3 on 2022-06-02 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Linkedin_Profils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vanityname', models.CharField(blank=True, default='NaN', max_length=200)),
                ('Nom', models.CharField(blank=True, default='NaN', max_length=200)),
                ('headline', models.CharField(blank=True, default='NaN', max_length=200)),
                ('location', models.CharField(blank=True, default='NaN', max_length=200)),
                ('Lien_Linkedin', models.CharField(blank=True, default='NaN', max_length=200)),
            ],
        ),
    ]