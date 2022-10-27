from django.db import models
from django.conf import settings

from enum import Enum

class Status(str, Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'
    
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)
    
    def __str__(self):
        return self.value

class Item(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255,choices=Status.choices())
    
    def __str__(self):
        return self.status
