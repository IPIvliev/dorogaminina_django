from django.shortcuts import render
from .forms import SignUpForm, LoginForm
 
def index(request):
  if request.method == 'POST': 
    pass
  else:
    return render(request, "home/index.html", {
      'title': "Велопробег Дорога Минина 2022",
      'registrationform': SignUpForm,
      'loginform': LoginForm
    })

def about(request):
    return render(request, "home/about.html")

def contacts(request):
    return render(request, "home/contacts.html")