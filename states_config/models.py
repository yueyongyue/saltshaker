from django.db import models
from django.contrib.auth.models import User

from account.models import Businesses,UserProfiles

class Highstate(models.Model):
    name          =   models.CharField(max_length=50,unique=True)
    business      =   models.ManyToManyField(Businesses)
    content       =   models.TextField()
    informations  =   models.CharField(max_length=200)
    enabled       =   models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

