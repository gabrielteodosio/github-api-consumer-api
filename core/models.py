from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=False)
    access_token = models.CharField(max_length=255, null=False)

    avatar_url = models.TextField()
