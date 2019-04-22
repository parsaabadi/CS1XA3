from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CountryCapitalData(models.Model):
    country = models.CharField(max_length=200)
    capitals = models.CharField(max_length=200)

    def __str__(self):
        return self.country + ': ' + self.capitals
