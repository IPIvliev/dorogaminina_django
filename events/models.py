from django.db import models
from home.models import User

class Event(models.Model):
  event_name = models.CharField(max_length=100)
  start_date = models.DateField()
  price = models.IntegerField(default=0)
  addition_price = models.IntegerField(default=0)
  active = models.BooleanField(default=False)

  def __str__(self):
    return u'{0}'.format(self.event_name)

class Partner(models.Model):
  partner_name = models.CharField(max_length=100)
  partner_logo = models.FileField(upload_to='uploads/partners/')
  partner_link = models.CharField(max_length=100, null=True, blank=True)
  active = models.BooleanField(default=False)

class Place(models.Model):
  place_name = models.CharField(max_length=100)
  place_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  amount = models.IntegerField(default=0)
  active = models.BooleanField(default=False)

  def __str__(self):
    return u'{0}'.format(self.place_name)

class Merch(models.Model):
  merch_name = models.CharField(max_length=100, null=True, blank=True)
  merch_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  size = models.CharField(max_length=100, null=True, blank=True)
  merch_image = models.FileField(upload_to='uploads/merchs/', null=True, blank=True)
  active = models.BooleanField(default=False)
  def __str__(self):
    return u'{0}'.format(self.merch_name)

class Order(models.Model):
  order_event = models.ForeignKey(Event, on_delete=models.CASCADE)
  order_user = models.ForeignKey(User, on_delete=models.CASCADE)
  order_place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.PROTECT)
  order_merch = models.ForeignKey(Merch, null=True, blank=True, on_delete=models.PROTECT)
  price = models.IntegerField(default=0)
  comment = models.CharField(max_length=250, null=True, blank=True)
  active = models.BooleanField(default=False)