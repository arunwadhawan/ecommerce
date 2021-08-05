from django.contrib import admin

# Register your models here.

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'slug')

class ProductAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'price','stock','category','is_available', 'digital' )

admin.site.register(Customer)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
