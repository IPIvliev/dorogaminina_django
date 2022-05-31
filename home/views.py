from django.shortcuts import render
from .forms import SignUpForm, LoginForm
 
def index(request):
  if request.method == 'POST': 
    form = SignUpForm(request.POST)
    print("heeeeello")
    if form.is_valid():
      form.save()
      return render(request, "account/profile.html")

  else:
    return render(request, "home/index.html", {
      'title': "Велопробег Дорога Минина 2022",
      'registrationform': SignUpForm,
      'loginform': LoginForm
    })

def about(request):
    return render(request, "home/about.html")

def prog(request):
    return render(request, "home/prog.html")

def blog(request):
    return render(request, "home/blog.html")

def contacts(request):
    return render(request, "home/contacts.html")

def profile(request):
    return render(request, "account/profile.html")