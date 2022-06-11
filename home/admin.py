from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'lastname', 'username', 'middlename')
    search_fields = ['phone', 'lastname', 'username', 'middlename']

admin.site.register(User, UserAdmin)