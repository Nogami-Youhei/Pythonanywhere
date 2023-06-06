from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Paper(models.Model):
    keywords = models.CharField(max_length=100)
    number = models.IntegerField()
    ja = models.IntegerField()
    choices = models.CharField(max_length=100)