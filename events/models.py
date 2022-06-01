from django.db import models
from home.models import User

class Event(models.Model):
  event_name = models.CharField(max_length=100)
  start_date = models.DateField()
  price = models.IntegerField(default=0)
  addition_price = models.IntegerField(default=0)
  active = models.BooleanField(default=False)

class Partner(models.Model):
  partner_name = models.CharField(max_length=100)
  partner_logo = models.FileField(upload_to='uploads/partners/')
  partner_link = models.CharField(max_length=100, null=True, blank=True)
  active = models.BooleanField(default=False)

class Order(models.Model):
  order_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  order_user = models.ForeignKey(User, on_delete=models.CASCADE)
  price = models.IntegerField(default=0)
  active = models.BooleanField(default=False)