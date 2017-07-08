from django.db import models

class Test(models.Model):
    about = models.TextField(help_text="Text")