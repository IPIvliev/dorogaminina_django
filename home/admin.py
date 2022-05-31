from django.contrib import admin
from .models import User
from .forms import SignUpForm

admin.site.register(User)
