from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random, string

from events.models import Event, Partner, Order
from robokassa.forms import RobokassaForm
 
def index(request):
  if request.method == 'POST': 
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      more = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(5))
      user.more = more
      user.set_password(more)
      user.save()
      login(request, user)
      return render(request, "account/profile.html")
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
    return render(request, "home/about.html")

def prog(request):
    return render(request, "home/prog.html")

def blog(request):
    return render(request, "home/blog.html")

def contacts(request):
    return render(request, "home/contacts.html")

@login_required
def profile(request):
  active_event = Event.objects.get(active=True)
  if request.GET.get('delivery') == "true":
    print("Delivery True")
    order = Order.objects.get(order_event=active_event, order_user=request.user)
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
    order, created = Order.objects.get_or_create(order_event=active_event, order_user=request.user)
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

  return render(request, "account/profile.html", {'price_form': price_form, 'order': order, 'event': active_event})