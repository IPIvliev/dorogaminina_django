import logging

from django.http import HttpResponse
from django.shortcuts import redirect
from events.models import Order
from home.views import profile

from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
ROBOKASSA_INV_ID_OFFSET = 3000


def _payment_data(request):
  return request.POST if request.method == "POST" else request.GET


def _activate_order_by_inv_id(inv_id):
  order_id = int(inv_id) - ROBOKASSA_INV_ID_OFFSET
  order = Order.objects.get(id=order_id)
  order.active = True
  order.save(update_fields=["active"])
  return order


@csrf_exempt
def payment_received(request):
  data = _payment_data(request)
  inv_id = data.get("InvId")
  _activate_order_by_inv_id(inv_id)
  return HttpResponse(f"OK{inv_id}")

@csrf_exempt
def payment_success(request):
  data = _payment_data(request)
  inv_id = data.get("InvId")
  try:
    _activate_order_by_inv_id(inv_id)
  except (TypeError, ValueError, Order.DoesNotExist):
    logger.exception("Failed to activate order after Robokassa success callback.")
  return redirect(profile)

@csrf_exempt
def payment_fail(request):
  return redirect(profile)
