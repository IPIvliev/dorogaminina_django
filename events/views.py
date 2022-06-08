from django.shortcuts import render, redirect
from django.dispatch import receiver
from events.models import Order
from home.views import index

from django.http import HttpResponse
from robokassa.signals import result_received, success_page_visited, fail_page_visited
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_received(request, sender, **kwargs):
  print(kwargs)
  order = Order.objects.get(id=kwargs['InvId'])
  order.active = True
  order.price = kwargs['OutSum']
  order.save()
  return redirect(index)

@csrf_exempt
def payment_success(request):
  data = request.POST if USE_POST else request.GET
  form = SuccessRedirectForm(data)
  if form.is_valid():
    inv_id, out_sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']
    order = Order.objects.get(id=inv_id)
    order.active = True
    order.price = out_sum
    order.save()
    return redirect(index)

@csrf_exempt
def payment_fail(sender, **kwargs):
  return redirect(index)