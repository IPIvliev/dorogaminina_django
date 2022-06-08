"""dorogaminina_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from home import views
from events.views import payment_success, payment_fail, payment_received

urlpatterns = [
  path('', views.index),
  path('index.html', views.index),
  path('about.html', views.about, name='about'),
  path('prog.html', views.prog, name='prog'),
  path('blog.html', views.blog, name='blog'),
  path('contacts.html', views.contacts, name='contacts'),
  path('profile.html', views.profile, name='profile'),
  path('admin/', admin.site.urls),
  path('login.html', views.login_form, name='login'),
  path('logout.html', views.logout_form, name='logout'),
  path('/robokassa/success', payment_success),
  path('/robokassa/fail', payment_fail),
  path('/robokassa/paid', payment_received),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)