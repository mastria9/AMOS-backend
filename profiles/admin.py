from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile



class UsersInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)
    list_display = list(set([field.name for field in User._meta.fields])-set(["password",]))

admin.site.unregister(User)
admin.site.register(User,UserAdmin)





# class RequestAdmin(ModelAdmin):
#     list_display =  ('timestamp','referrer','ip_address','method','path','session_key')
#     search_fields = ('timestamp','referrer','ip_address','method','path','session_key')
# admin.site.register(Request,RequestAdmin)
