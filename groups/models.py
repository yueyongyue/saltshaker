from django.db import models
from django.contrib.auth.models import User
from minions.models import Minions_status

# Create your models here.

class Groups(models.Model):
    name          =   models.CharField(max_length=50,unique=True)
    business      =   models.CharField(max_length=100)
    informations  =   models.CharField(max_length=200)
    enabled       =   models.BooleanField(default=True)
    # the user who own the group
    #owner         =   models.ForeignKey(User,related_name="groups_owner")
    owner         =   models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related")
    privileges    =   models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Hosts(models.Model):
    minion =    models.ForeignKey(Minions_status,related_name="%(app_label)s_%(class)s_related")
    name          =    models.CharField(max_length=50,unique=True)
    business      =    models.CharField(max_length=100)
    informations  =    models.CharField(max_length=200)
    group         =    models.ForeignKey(Groups)
    enabled       =    models.BooleanField(default=True)
    #owner         =   models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related")
    privileges    =    models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

