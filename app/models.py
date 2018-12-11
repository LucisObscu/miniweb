from django.db import models

# Create your models here.

class Clien(models.Model):
    title = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    hit = models.CharField(max_length=20)
    time = models.CharField(max_length=100)
    link = models.CharField(max_length=100)