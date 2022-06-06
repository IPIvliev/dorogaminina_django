from django.contrib import admin
from .models import Event, Partner, Order, Place, Merch

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_user', 'order_event', 'active')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'start_date', 'active')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'partner_order')

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'place_event', 'amount', 'busy', 'free', 'active')
    readonly_fields = ('free', 'busy')

@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    list_display = ('merch_name', 'size', 'merch_event', 'active')