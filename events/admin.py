from django.contrib import admin
from .models import Event, Partner, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_user', 'order_event', 'active')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'start_date', 'active')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('partner_name',)
