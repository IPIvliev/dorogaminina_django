from django.shortcuts import render
from django.dispatch import receiver
from smsru.signals import smsru_call_back_sms

@receiver(smsru_call_back_sms)
def call_back_sms(sender, instance, new_status, *args, **kwargs):
    instance.msg = 'signal'
    instance.save()