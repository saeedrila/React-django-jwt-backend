from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'phone', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email','id','username', 'phone',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'password1', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)