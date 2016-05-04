from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Businesses(models.Model):
    name          =    models.CharField(max_length=50,unique=True)
    informations  =    models.CharField(max_length=200)
    enabled       =    models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class Privileges(models.Model):
    name          =    models.CharField(max_length=50,unique=True)
    deny          =    models.CharField(max_length=250,default='')
    allow         =    models.CharField(max_length=250,default='')
    informations  =    models.CharField(max_length=200)
    enabled       =    models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class UserProfiles(models.Model):
    user          =   models.OneToOneField(User,on_delete = models.CASCADE)
    department    =   models.CharField(max_length = 100)
    telephone     =   models.CharField(max_length = 50)
    privilege     =   models.ManyToManyField(Privileges)
    business      =   models.ManyToManyField(Businesses)
