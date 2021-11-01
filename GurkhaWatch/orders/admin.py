from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'amount_paid', 'status']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'phone_number',
                    'email', 'order_total', 'service_charge', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'phone_number',
                     'email']
    list_per_page = 20


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'product',
                    'quantity', 'ordered', 'created_at']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
