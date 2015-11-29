from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClusterData(models.Model):
    cluster_num = models.IntegerField
    dir_name = models.CharField(max_length=30)
    owner = models.ForeignKey(User)