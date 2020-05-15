from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    access_token = models.CharField(max_length=255, null=False)

    avatar_url = models.TextField()
