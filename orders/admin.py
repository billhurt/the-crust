from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('line_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'order_type', 'status', 'total', 'is_paid', 'created_at')
    list_filter = ('status', 'order_type', 'is_paid')
    list_editable = ('status',)
    readonly_fields = ('subtotal', 'delivery_charge', 'total', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
