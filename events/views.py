from django.shortcuts import render, redirect
from django.dispatch import receiver
from events.models import Order
from home.views import index

from django.http import HttpResponse
from robokassa.signals import result_received, success_page_visited, fail_page_visited

def payment_received(sender, **kwargs):
  order = Order.objects.get(id=kwargs['InvId'])
  order.active = True
  order.price = kwargs['OutSum']
  order.save()
  return redirect(index)

result_received.connect(payment_received)

def payment_success(sender, **kwargs):
  return redirect(index)

success_page_visited.connect(payment_success)

def payment_fail(sender, **kwargs):
  return redirect(index)

fail_page_visited.connect(payment_fail)