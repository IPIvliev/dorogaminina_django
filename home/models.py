from django.db import models
#from events.models import Event, Order
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from home.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255)
    lastname = models.CharField(_('lastname'), max_length=255)
    middlename = models.CharField(_('middlename'), max_length=255)
    more = models.CharField(_('more'), null=True, blank=True, max_length=5)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone = models.CharField(_('phone number'), max_length=30, null=False, blank=False, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    #events = models.ManyToManyField(Event)
    #orders = models.OneToOneField(Order, on_delete=models.CASCADE)
    is_verified = models.BooleanField(_('verified'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('username', 'email', 'phone')