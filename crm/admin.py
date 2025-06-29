from django.contrib import admin
from .models import Customer, Product, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    list_editable = ('price', 'stock')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'order_date', 'products_count')
    list_filter = ('order_date', 'created_at')
    search_fields = ('customer__name', 'customer__email')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    filter_horizontal = ('products',)
    ordering = ('-order_date',)
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Products Count'