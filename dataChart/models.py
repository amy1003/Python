

# Create your models here.

# 建立 ORM映射
from django.db import models

class Poptbl(models.Model):
    pref_name = models.CharField(max_length=30)
    population = models.IntegerField()
