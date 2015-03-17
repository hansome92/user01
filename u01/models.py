from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateField()
    random = models.IntegerField(default=0)


# Create your models here.
