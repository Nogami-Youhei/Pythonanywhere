from django.db import models
from django.utils import timezone

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Paper(models.Model):
    user = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    keywords = models.CharField(max_length=100)
    number = models.IntegerField()
    ja = models.IntegerField()
    choices = models.CharField(max_length=100)
