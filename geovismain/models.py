import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    group = models.ForeignKey('Group')
    def __unicode__(self):
        return self.name

class Dataset(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=150)
    infopath = models.CharField(max_length=150)
    def __unicode__(self):
        return self.name
    
    