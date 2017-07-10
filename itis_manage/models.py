from django.db import models


class Test(models.Model):
    about = models.TextField(help_text="Text")


class Person(models.Model):
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    third_name = models.CharField(max_length=40)
    birth_date = models.CharField(max_length=40, null=True, blank=True)

