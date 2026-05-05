from django.shortcuts import render, redirect
from home.forms import SignUpForm, LoginForm
from events.forms import FinalOrderForm, MessageForm
from events.models import Place, Event, Partner, Order
from blog.models import Article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
import logging
import random, string
from django.core.paginator import Paginator

from robokassa.forms import RobokassaForm
from home.password_delivery import send_registration_password

logger = logging.getLogger(__name__)

def render_index(request, registrationform=SignUpForm):
  event = Event.objects.get(active='True')
  return render(request, "home/index.html", {
    'title': event.event_name,
    'registrationform': registrationform,
    'partners': Partner.objects.filter(active=True).order_by('partner_order'),
    'event': event
  })

def index(request):
  if request.method == 'POST': 
    form = SignUpForm(request.POST)
    if form.is_valid():
      try:
        with transaction.atomic():
          user = form.save()
          more = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(5))
          user.more = more
          user.set_password(more)
          user.save()
          send_registration_password(user)
      except Exception:
        logger.exception("Failed to deliver registration password.")
        form.add_error(None, "Не удалось отправить пароль. Проверьте настройки доставки пароля или попробуйте позже.")
        return render_index(request, form)
      login(request, user)
      return redirect(profile)
    else:
      print("Registration Form is not valid")
      return render_index(request, form)
  else:
    return render_index(request)

def login_form(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      phone = form.cleaned_data['phone']
      password = form.cleaned_data['password']
      user = authenticate(request, username=phone, password=password)
      if user is None:
        return render(request, "home/signin.html", {
          'loginform': LoginForm
        })
      else:
        login(request, user)
        return redirect(profile)
    else:
      print("Form is not valid")
  else:
    if request.user.is_authenticated:
      return redirect(profile)
    else:
      return render(request, "home/signin.html", {
        'loginform': LoginForm
      })

def logout_form(request):
  logout(request)
  return redirect(index)

def about(request):
  active_event = Event.objects.get(active=True)
  return render(request, "home/about.html", { 
    'title': active_event.event_name,
    'event': active_event,
    'registrationform': SignUpForm,
  })

def prog(request):
  active_event = Event.objects.get(active=True)
  return render(request, "home/prog.html", { 
    'title': active_event.event_name,
    'event': active_event,
    'registrationform': SignUpForm,
  })

def blog(request):
  active_event = Event.objects.get(active=True)
  news = Article.objects.order_by('-publish')
  if request.GET.get('category') == "news":
    news = Article.objects.filter(category=1).order_by('-publish')
  if request.GET.get('category') == "history":
    news = Article.objects.filter(category=2).order_by('-publish')
  paginator = Paginator(news, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, "home/blog.html", {
    'page_obj': page_obj,
    'event': active_event
  })

def contacts(request):
  active_event = Event.objects.get(active=True)
  if request.method == 'POST': 
    form = MessageForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(contacts)
    else:
      return redirect(contacts)
  else:
    return render(request, "home/contacts.html", {
      'event': active_event,
      'messageform': MessageForm
  })

@login_required
def profile(request):
  active_event = Event.objects.get(active=True)
  order, created = Order.objects.get_or_create(order_event=active_event, order_user=request.user)
  finalorderform = FinalOrderForm(event=active_event, order=order )
  fio = '%s %s %s %s' % (request.user.id, request.user.lastname, request.user.username, request.user.middlename)

  if order.active == False:

    if request.GET.get('delivery') == "true":
      price = active_event.price - active_event.addition_price
    else:
      price = active_event.price
    
    order.price = price
    order.save()

  price_form = RobokassaForm(initial={
            'OutSum': order.price,
            'InvId': 3000 + order.id,
            'Desc': fio,
        })


  if request.method == 'POST':
    form = FinalOrderForm(request.POST, event=active_event, order=order)
    if form.is_valid():
      order.order_merch = form.cleaned_data['order_merch']
      order.order_place = form.cleaned_data['order_place']
      order.comment = form.cleaned_data['comment']
      order.save()
      place = Place.objects.get(id=order.order_place.id)
      place.save()

  return render(request, "account/profile.html", {'price_form': price_form, 'order': order, 'event': active_event, 'finalorderform': finalorderform})
