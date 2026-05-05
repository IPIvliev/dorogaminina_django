from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from smsru.service import SmsRuApi


PASSWORD_DELIVERY_SMS = "sms"
PASSWORD_DELIVERY_EMAIL = "email"


def build_password_message(user):
    return "Ваш пароль для Дороги Минина: " + user.more


def send_registration_password(user):
    method = getattr(settings, "PASSWORD_DELIVERY_METHOD", PASSWORD_DELIVERY_SMS)
    message = build_password_message(user)

    if method == PASSWORD_DELIVERY_SMS:
        api = SmsRuApi()
        api.send_one_sms(user.phone, message)
        return

    if method == PASSWORD_DELIVERY_EMAIL:
        if not user.email:
            raise ValueError("User email is required for password delivery by email.")

        send_mail(
            getattr(settings, "PASSWORD_DELIVERY_EMAIL_SUBJECT", "Пароль для Дороги Минина"),
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return

    raise ImproperlyConfigured(
        "PASSWORD_DELIVERY_METHOD must be 'sms' or 'email'."
    )
