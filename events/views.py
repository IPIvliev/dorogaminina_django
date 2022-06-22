from django.shortcuts import redirect
from events.models import Order
from home.views import profile

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_received(request):
  data = request.POST
  print("Request from payment_received")
  print(data)
  inv_id = data.get("InvId")
  order = Order.objects.get(id=inv_id)
  order.active = True
  order.save()
  return redirect(profile)

@csrf_exempt
def payment_success(request):
  data = request.POST
  print("Request from payment_success")
  print(data)
  inv_id = data.get("InvId")
  order = Order.objects.get(id=inv_id)
  order.active = True
  order.save()
  return redirect(profile)

@csrf_exempt
def payment_fail(sender, **kwargs):
  return redirect(profile)