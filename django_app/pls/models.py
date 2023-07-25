from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     pass


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Paper(models.Model):
    order = (
        ("1", "ヒット率"),
        ("5", "発行日[新しい順]"),
        ("6", "発行日[古い順]"),
        ("2", "公開日[新しい順]"),
        ("3", "公開日[古い順]"),
        ("4", "資料名順"),
        )
    user = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    keywords = models.CharField(max_length=100)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    ja = models.BooleanField()
    choices = models.CharField(max_length=100, choices=order, default=("5", "発行日[新しい順]"))