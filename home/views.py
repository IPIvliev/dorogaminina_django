from django.shortcuts import render
from .forms import SignUpForm, LoginForm

from django.dispatch import receiver
from phone_auth.signals import verify_phone
 
def index(request):
    return render(request, "home/index.html", {
      'title': "Велопробег Дорога Минина 2022",
      'registrationform': SignUpForm,
      'loginform': LoginForm
    })

def about(request):
    return render(request, "home/about.html")

def contacts(request):
    return render(request, "home/contacts.html")