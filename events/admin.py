from django.contrib import admin
from .models import Event, Partner, Order, Place, Merch, Message
from django import forms
from ckeditor.widgets import CKEditorWidget
from import_export.admin import ExportMixin, ExportActionMixin
from import_export import resources

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('order_user__id', 'order_user__phone', 'order_user__lastname', 'order_user__username', 'order_user__middlename', 'order_place__place_name', 'order_merch__merch_name', 'active')
        export_order = ('order_user__id', 'order_user__phone', 'order_user__lastname', 'order_user__username', 'order_user__middlename', 'order_place__place_name', 'order_merch__merch_name', 'active')

@admin.register(Order)
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'order_user', 'get_user_id', 'get_user', 'order_place', 'order_merch', 'price', 'active')
    list_filter = ('active', 'order_event__event_name')
    search_fields = ['id', 'order_user__username', 'order_user__lastname', 'order_user__middlename', 'order_user__phone']

    @admin.display(description='ФИО участника')
    def get_user(self, obj):
        return '%s %s' % (obj.order_user.lastname, obj.order_user.username)

    @admin.display(description='ID участника')
    def get_user_id(self, obj):
        return '%s' % (obj.order_user.id)
    
class EventAdminForm(forms.ModelForm):
    about = forms.CharField(widget=CKEditorWidget())
    prog = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = '__all__'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  form = EventAdminForm
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

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')