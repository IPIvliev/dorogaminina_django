from django.shortcuts import render
from django.dispatch import receiver
from events.models import Order

from django.http import HttpResponse
from robokassa.signals import result_received, success_page_visited, fail_page_visited

def payment_received(sender, **kwargs):
  order = Order.objects.get(id=kwargs['InvId'])
  order.active = True
  order.price = kwargs['OutSum']
  order.save()
  return HttpResponse('<h1>Hello HttpResponse</h1>')

result_received.connect(payment_received)

def payment_success(sender, **kwargs):
  return HttpResponse('<h1>Paiment Success</h1>')

success_page_visited.connect(payment_success)

def payment_fail(sender, **kwargs):
  return HttpResponse('<h1>Paiment Fail</h1>')

fail_page_visited.connect(payment_fail)