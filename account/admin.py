from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    list_dispaly=('email','username')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    
admin.site.register(User,UserAdmin)
# Register your models here.
