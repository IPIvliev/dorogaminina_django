import logging
from hashlib import md5

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.crypto import constant_time_compare
from events.models import Order
from home.views import profile

from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
ROBOKASSA_INV_ID_OFFSET = 3000


def _payment_data(request):
  return request.POST if request.method == "POST" else request.GET


def _get_payment_param(data, name):
  return data.get(name) or data.get(name.upper()) or data.get(name.lower())


def _signature_is_valid(data, password):
  out_sum = _get_payment_param(data, "OutSum")
  inv_id = _get_payment_param(data, "InvId")
  signature = _get_payment_param(data, "SignatureValue")
  if not out_sum or not inv_id or not signature:
    return False
  signature_base = f"{out_sum}:{inv_id}:{password}"
  expected = md5(signature_base.encode("utf-8")).hexdigest()
  return constant_time_compare(expected.lower(), signature.lower())


def _log_callback(request, callback_type, inv_id, status, reason=""):
  logger.info(
    "Robokassa %s callback: status=%s inv_id=%s reason=%s method=%s remote_addr=%s user_agent=%s",
    callback_type,
    status,
    inv_id,
    reason,
    request.method,
    request.META.get("REMOTE_ADDR", ""),
    request.META.get("HTTP_USER_AGENT", ""),
  )


def _activate_order_by_inv_id(inv_id):
  order_id = int(inv_id) - ROBOKASSA_INV_ID_OFFSET
  order = Order.objects.get(id=order_id)
  order.active = True
  order.save(update_fields=["active"])
  return order


@csrf_exempt
def payment_received(request):
  data = _payment_data(request)
  inv_id = _get_payment_param(data, "InvId")
  if not _signature_is_valid(data, settings.ROBOKASSA_PASSWORD2):
    _log_callback(request, "result", inv_id, "rejected", "invalid_signature")
    return HttpResponseBadRequest("Invalid signature")

  try:
    _activate_order_by_inv_id(inv_id)
  except (TypeError, ValueError):
    _log_callback(request, "result", inv_id, "rejected", "invalid_inv_id")
    return HttpResponseBadRequest("Invalid InvId")
  except Order.DoesNotExist:
    _log_callback(request, "result", inv_id, "rejected", "order_not_found")
    return HttpResponseNotFound("Order not found")

  _log_callback(request, "result", inv_id, "accepted")
  return HttpResponse(f"OK{inv_id}")

@csrf_exempt
def payment_success(request):
  data = _payment_data(request)
  inv_id = _get_payment_param(data, "InvId")
  if _signature_is_valid(data, settings.ROBOKASSA_PASSWORD1):
    try:
      _activate_order_by_inv_id(inv_id)
      _log_callback(request, "success", inv_id, "accepted")
    except (TypeError, ValueError):
      _log_callback(request, "success", inv_id, "rejected", "invalid_inv_id")
    except Order.DoesNotExist:
      _log_callback(request, "success", inv_id, "rejected", "order_not_found")
  else:
    _log_callback(request, "success", inv_id, "rejected", "invalid_signature")
  return redirect(profile)

@csrf_exempt
def payment_fail(request):
  return redirect(profile)
