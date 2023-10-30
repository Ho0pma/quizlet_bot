from django.db import models


class Library(models.Model):
   username = models.CharField(max_length=255)
   word = models.CharField(max_length=255)
   definition = models.TextField()
   url = models.CharField(max_length=255)
   shared = models.CharField(max_length=255)


class Swag(models.Model):
   username = models.CharField(max_length=255)
   comment = models.CharField(max_length=255)
