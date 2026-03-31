from django.shortcuts import render
from .models import Category, MenuItem


def menu(request):
    categories = Category.objects.prefetch_related('items').all()
    # Only show categories that have at least one available item
    categories = [c for c in categories if c.items.filter(is_available=True).exists()]
    featured = MenuItem.objects.filter(is_featured=True, is_available=True)[:4]
    return render(request, 'menu/menu.html', {
        'categories': categories,
        'featured': featured,
    })
