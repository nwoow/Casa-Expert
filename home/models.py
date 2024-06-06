from django.db import models

# Create your models here.
class Estimate(models.Model):
    name =models.CharField(max_length=180)
    email = models.CharField(max_length=220)
    city_name = models.CharField(max_length=110)
    service = models.CharField(max_length=220)
    message = models.TextField()


class Contact(models.Model):
    name =models.CharField(max_length=180)
    email = models.CharField(max_length=220)
    phone = models.CharField(max_length=220)
    subject = models.CharField(max_length=220)
    message = models.TextField()


class NewAccount(models.Model):
    phone = models.CharField(max_length=220)