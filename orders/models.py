from django.db import models
from menu.models import MenuItem


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Collection'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    ORDER_TYPE_CHOICES = [
        ('collection', 'Collection'),
        ('delivery', 'Delivery'),
    ]

    # Customer details
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    # Delivery details (optional for collection)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='collection')
    delivery_address = models.TextField(blank=True)
    delivery_notes = models.TextField(blank=True)

    # Order state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Payment (Stripe-ready)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    is_paid = models.BooleanField(default=False)

    # Totals
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.customer_name}'

    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items.all())
        self.delivery_charge = 2.50 if self.order_type == 'delivery' else 0
        self.total = self.subtotal + self.delivery_charge
        self.save(update_fields=['subtotal', 'delivery_charge', 'total'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.menu_item.name}'

    @property
    def line_total(self):
        return self.unit_price * self.quantity
