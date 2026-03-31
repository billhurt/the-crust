from menu.models import MenuItem
from decimal import Decimal


class Cart:
    """Session-based cart."""

    SESSION_KEY = 'cart'
    DELIVERY_CHARGE = Decimal('2.50')

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if cart is None:
            cart = {}
            self.session[self.SESSION_KEY] = cart
        self.cart = cart

    def add(self, item_id, quantity=1):
        item_id = str(item_id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] += quantity
        else:
            item = MenuItem.objects.get(pk=item_id)
            self.cart[item_id] = {
                'quantity': quantity,
                'price': str(item.price),
                'name': item.name,
            }
        self._save()

    def update(self, item_id, quantity):
        item_id = str(item_id)
        if quantity <= 0:
            self.remove(item_id)
        else:
            if item_id in self.cart:
                self.cart[item_id]['quantity'] = quantity
                self._save()

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self._save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True
        self.cart = {}

    def _save(self):
        self.session.modified = True

    def __iter__(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(pk__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.pk)]['item'] = item
        for entry in cart.values():
            entry['price'] = Decimal(entry['price'])
            entry['line_total'] = entry['price'] * entry['quantity']
            yield entry

    def __len__(self):
        return sum(entry['quantity'] for entry in self.cart.values())

    @property
    def subtotal(self):
        return sum(Decimal(e['price']) * e['quantity'] for e in self.cart.values())

    def total(self, order_type='collection'):
        charge = self.DELIVERY_CHARGE if order_type == 'delivery' else Decimal('0')
        return self.subtotal + charge
