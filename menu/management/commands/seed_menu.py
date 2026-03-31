from django.core.management.base import BaseCommand
from django.utils.text import slugify
from menu.models import Category, MenuItem


MENU_DATA = [
    {
        'name': 'Pizzas',
        'order': 1,
        'items': [
            {
                'name': 'Margherita',
                'description': 'San Marzano tomato, fior di latte mozzarella, fresh basil, extra virgin olive oil.',
                'price': '10.00',
                'is_featured': True,
            },
            {
                'name': 'Pepperoni',
                'description': 'Tomato base, mozzarella, generous slices of spicy pepperoni.',
                'price': '12.00',
                'is_featured': True,
            },
            {
                'name': 'BBQ Chicken',
                'description': 'Smoky BBQ base, mozzarella, grilled chicken, red onion, fresh coriander.',
                'price': '13.00',
            },
            {
                'name': 'Fungi e Tartufo',
                'description': 'Cream base, mozzarella, mixed wild mushrooms, truffle oil, parsley.',
                'price': '13.50',
                'is_featured': True,
            },
            {
                'name': 'Four Cheese',
                'description': 'Mozzarella, gorgonzola, taleggio and parmesan. A proper cheese lover\'s pizza.',
                'price': '13.00',
            },
            {
                'name': 'The Farm Special',
                'description': 'Tomato, mozzarella, nduja, roasted peppers, caramelised onion, fresh rocket.',
                'price': '14.00',
                'is_featured': True,
            },
        ],
    },
    {
        'name': 'Sides',
        'order': 2,
        'items': [
            {
                'name': 'Garlic Dough Balls',
                'description': 'Six pillowy dough balls, garlic butter, fresh parsley.',
                'price': '4.50',
            },
            {
                'name': 'Rocket & Parmesan Salad',
                'description': 'Wild rocket, shaved parmesan, lemon dressing.',
                'price': '4.00',
            },
            {
                'name': 'Chips',
                'description': 'Skin-on fries, sea salt.',
                'price': '3.50',
            },
        ],
    },
    {
        'name': 'Drinks',
        'order': 3,
        'items': [
            {
                'name': 'San Pellegrino (330ml)',
                'description': 'Sparkling mineral water.',
                'price': '1.80',
            },
            {
                'name': 'Coke (330ml)',
                'description': 'Ice cold Coca-Cola.',
                'price': '2.00',
            },
            {
                'name': 'Lemonade (330ml)',
                'description': 'Refreshing still lemonade.',
                'price': '2.00',
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample menu data for The Crust'

    def handle(self, *args, **options):
        self.stdout.write('Seeding menu...')
        for cat_data in MENU_DATA:
            category, _ = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={'name': cat_data['name'], 'order': cat_data['order']},
            )
            for item_data in cat_data['items']:
                MenuItem.objects.get_or_create(
                    slug=slugify(item_data['name']),
                    defaults={
                        'category': category,
                        'name': item_data['name'],
                        'description': item_data.get('description', ''),
                        'price': item_data['price'],
                        'is_featured': item_data.get('is_featured', False),
                        'is_available': True,
                    },
                )
        self.stdout.write(self.style.SUCCESS('Menu seeded successfully!'))
