from django.db import models


class Linkedin_Profils(models.Model):
    vanityname = models.CharField(max_length=200, blank=True, default='NaN')
    Nom = models.CharField(max_length=200, blank=True, default='NaN')
    headline = models.CharField(max_length=200, blank=True, default='NaN')
    location = models.CharField(max_length=200, blank=True, default='NaN')
    Lien_Linkedin = models.CharField(max_length=200, blank=True, default='NaN')
    industryName=models.CharField(max_length=200, blank=True, default='NaN')
    experience=models.CharField(max_length=200, blank=True, default='NaN')
    education=models.CharField(max_length=200, blank=True, default='NaN')


class linkedin_account(models.Model):
    email=models.EmailField(default='exemple@exemple.com')
    password=models.CharField(max_length=500,default='password')

    def __str__(self):
        return self.email
