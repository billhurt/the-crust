from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_featured', 'order')
    list_filter = ('category', 'is_available', 'is_featured')
    list_editable = ('price', 'is_available', 'is_featured', 'order')
    prepopulated_fields = {'slug': ('name',)}
