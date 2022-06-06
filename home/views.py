from django.shortcuts import render, redirect
from home.forms import SignUpForm, LoginForm
from events.forms import FinalOrderForm
from events.models import Place
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random, string

from events.models import Event, Partner, Order
from robokassa.forms import RobokassaForm
from smsru.service import SmsRuApi
 
def index(request):
  if request.method == 'POST': 
    form = SignUpForm(request.POST)
    if form.is_valid():
      api = SmsRuApi()
      user = form.save()
      more = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(5))
      user.more = more
      user.set_password(more)
      user.save()
      print('Сохранили пользователя')
      message = 'Ваш пароль для Дороги Минина: ' + user.more
      api.send_one_sms(user.phone, message)
      print('Отправили смс')
      login(request, user)
      return redirect(profile)
  else:
    return render(request, "home/index.html", {
      'title': Event.objects.get(active='True').event_name,
      'registrationform': SignUpForm,
      'partners': Partner.objects.filter(active=True)
    })

def login_form(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      phone = form.cleaned_data['phone']
      password = form.cleaned_data['password']
      print(phone)
      print(password)
      user = authenticate(request, username=phone, password=password)
      if user is None:
        print("User not found")
        return render(request, "home/signin.html", {
          'loginform': LoginForm
        })
      else:
        login(request, user)
        return redirect(profile)
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
    'registrationform': SignUpForm,
  })

def prog(request):
  active_event = Event.objects.get(active=True)
  return render(request, "home/prog.html", { 
    'title': active_event.event_name,
    'registrationform': SignUpForm,
  })

def blog(request):
    return render(request, "home/blog.html")

def contacts(request):
    return render(request, "home/contacts.html")

@login_required
def profile(request):
  active_event = Event.objects.get(active=True)
  finalorderform = FinalOrderForm(event=active_event)
  order, created = Order.objects.get_or_create(order_event=active_event, order_user=request.user)
  if request.GET.get('delivery') == "true":
    print("Delivery True")
    # order = Order.objects.get(order_event=active_event, order_user=request.user)
    price = active_event.addition_price
    order.price = price
    order.save()
    price_form = RobokassaForm(initial={
              'OutSum': order.price,
              'InvId': request.user.id,
              'Desc': order.id,
              # 'IncCurrLabel': '',
              # 'Culture': 'ru'
          })
  else:
    print( request.GET.get('delivery'))
    # order, created = Order.objects.get_or_create(order_event=active_event, order_user=request.user)
    price = active_event.price
    order.price = price
    order.save()

    price_form = RobokassaForm(initial={
                'OutSum': order.price,
                'InvId': request.user.id,
                'Desc': order.id,
                # 'IncCurrLabel': '',
                # 'Culture': 'ru'
            })
  if request.method == 'POST':
    form = FinalOrderForm(request.POST)
    if form.is_valid():
      order.order_merch = form.cleaned_data['order_merch']
      order.order_place = form.cleaned_data['order_place']
      order.save()
      place = Place.objects.get(id=order.order_place.id)
      place.save()

  return render(request, "account/profile.html", {'price_form': price_form, 'order': order, 'event': active_event, 'finalorderform': finalorderform})