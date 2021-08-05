from django.contrib import admin
from django.contrib.auth import get_user_model
#from .models import User
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

class AccountAdmin(UserAdmin):
    search_fields = ('email','name')
    list_display = ('email','name','phone_number','is_active','is_staff','is_admin')
    list_filter = ('is_active','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','phone_number',)}),
        ('Permissions', {'fields': ('is_active','is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','phone_number', 'password1', 'password2','is_active','is_admin'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ()
# Register your models here.
admin.site.register(User, AccountAdmin)
