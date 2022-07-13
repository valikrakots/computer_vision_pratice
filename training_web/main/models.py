from django.contrib.auth.models import User
from django.db import models


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    res_text = models.TextField(default=None, blank=True, null=True)
    res_image = models.ImageField(upload_to='results/', default=None, blank=True, null=True)


class CalculationCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(User, default=0)
