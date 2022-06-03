from django.db import models


class Linkedin_Profils(models.Model):
    vanityname = models.CharField(max_length=200, blank=True, default='NaN')
    Nom = models.CharField(max_length=200, blank=True, default='NaN')
    headline = models.CharField(max_length=200, blank=True, default='NaN')
    location = models.CharField(max_length=200, blank=True, default='NaN')
    Lien_Linkedin = models.CharField(max_length=200, blank=True, default='NaN')