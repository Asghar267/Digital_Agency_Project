from django.contrib import admin
from .models import Service, Order, Customer, Cart 
from django.contrib.auth.models import User


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_title', 'price')

admin.site.register(Service, ServiceAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service',  'date_added')

admin.site.register(Cart, CartAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username',
                    'email', 'password', 'address')


admin.site.register(Customer, CustomerAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('USERNAME', 'EMAIL ADDRESS',
#                     'FIRST NAME', 'STAFF STATUS', 'PASSWORD')

# admin.site.register(User, UserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'status',
                     'order_date',  'orderitem')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__username', 'orderitem')


admin.site.register(Order, OrderAdmin)

