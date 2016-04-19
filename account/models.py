from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfiles(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    department = models.CharField(max_length = 100)
    telephone = models.CharField(max_length = 50)
    role = models.CharField(max_length = 100)
    business = models.CharField(max_length = 100)
