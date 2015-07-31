import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

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
    
    