from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import Cart
from .models import Order, OrderItem
from menu.models import MenuItem
import json


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    data = json.loads(request.body) if request.content_type == 'application/json' else {}
    quantity = int(data.get('quantity', 1))
    cart.add(item.pk, quantity)
    return JsonResponse({'cart_count': len(cart), 'message': f'{item.name} added to order'})


@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 0))
    cart.update(item_id, quantity)
    return JsonResponse({'cart_count': len(cart)})


@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return JsonResponse({'cart_count': len(cart)})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your order is empty.')
        return redirect('menu:menu')

    if request.method == 'POST':
        order_type = request.POST.get('order_type', 'collection')
        order = Order.objects.create(
            customer_name=request.POST['customer_name'],
            customer_email=request.POST['customer_email'],
            customer_phone=request.POST['customer_phone'],
            order_type=order_type,
            delivery_address=request.POST.get('delivery_address', ''),
            delivery_notes=request.POST.get('delivery_notes', ''),
        )
        for entry in cart:
            OrderItem.objects.create(
                order=order,
                menu_item=entry['item'],
                quantity=entry['quantity'],
                unit_price=entry['price'],
            )
        order.calculate_totals()
        cart.clear()
        # TODO: integrate Stripe payment here — create PaymentIntent and redirect to payment page
        return redirect('orders:confirmation', order_id=order.pk)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'delivery_charge': Cart.DELIVERY_CHARGE,
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/confirmation.html', {'order': order})
