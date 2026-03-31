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
                'description': 'Tomato sauce, basil, mozzarella.',
                'price': '8.50',
                'is_featured': True,
            },
            {
                'name': 'Prosciutto e Fungi',
                'description': 'Prosciutto and mushroom.',
                'price': '10.95',
                'is_featured': True,
            },
            {
                'name': 'Farmhouse Feast',
                'description': 'Farmhouse sausage, bacon, prosciutto, chicken.',
                'price': '11.95',
                'is_featured': True,
            },
            {
                'name': "Forager's Favourite",
                'description': 'Mushroom, peppers, onion, sweetcorn.',
                'price': '10.95',
            },
            {
                'name': 'Pollo Picante',
                'description': 'Chicken, peppers, fresh chilli.',
                'price': '10.95',
            },
            {
                'name': 'Pepperoni Americana',
                'description': 'Pepperoni and peppers.',
                'price': '10.95',
                'is_featured': True,
            },
            {
                'name': 'The Pen-y-ghent',
                'description': 'Sundried tomato and green pesto.',
                'price': '10.95',
            },
            {
                'name': 'La Rosa Bianca',
                'description': 'Cream base, mushrooms, finished with truffle dust, local honey and a fresh grating of Pecorino DOP.',
                'price': '10.95',
                'is_featured': True,
            },
            {
                'name': 'The Hot Hog',
                'description': "Nduja, farmhouse sausage, hot honey.",
                'price': '10.95',
            },
            {
                'name': 'Weekly Special',
                'description': "Ask us what the special of the week is — call us or drop us a message!",
                'price': '0.00',
            },
        ],
    },
    {
        'name': 'Garlic Bread',
        'order': 2,
        'items': [
            {
                'name': 'Garlic Bread 9"',
                'description': 'Available as cheese and tomato.',
                'price': '5.95',
            },
            {
                'name': 'Garlic Bread 12"',
                'description': 'Available as cheese and tomato.',
                'price': '6.95',
            },
        ],
    },
    {
        'name': 'Salads',
        'order': 3,
        'items': [
            {
                'name': 'Caesar Salad',
                'description': 'Chicken, cucumber, lettuce, red onion, bacon, Caesar dressing, finished with croutons, black pepper and parmesan. Available gluten free with crispy bacon bits instead of croutons.',
                'price': '6.50',
            },
            {
                'name': 'House Salad',
                'description': 'Lettuce, red onion, cucumber, cherry tomatoes, finished with extra virgin olive oil.',
                'price': '4.95',
            },
        ],
    },
    {
        'name': 'Dough Balls',
        'order': 4,
        'items': [
            {
                'name': 'Garlic Butter Dough Balls',
                'description': 'Classic garlic butter.',
                'price': '4.95',
            },
            {
                'name': 'Bacon Dough Balls',
                'description': 'Topped with bacon.',
                'price': '5.95',
            },
            {
                'name': 'Pepperoni Dough Balls',
                'description': 'Topped with pepperoni.',
                'price': '5.95',
            },
            {
                'name': 'Cheese & Garlic Dough Balls',
                'description': 'Cheese and garlic.',
                'price': '5.95',
            },
            {
                'name': 'Cheese Dough Balls',
                'description': 'Topped with melted cheese.',
                'price': '5.95',
            },
        ],
    },
    {
        'name': 'Sides',
        'order': 5,
        'items': [
            {
                'name': 'Sweet Potato Fries',
                'description': 'Crispy sweet potato fries.',
                'price': '3.50',
            },
            {
                'name': 'Skin-on Fries',
                'description': 'Rustic skin-on fries.',
                'price': '2.50',
            },
        ],
    },
    {
        'name': 'Dips',
        'order': 6,
        'items': [
            {
                'name': 'Mayo',
                'description': 'Classic mayonnaise.',
                'price': '1.00',
            },
            {
                'name': 'Heinz Tomato Ketchup',
                'description': 'The classic.',
                'price': '1.00',
            },
            {
                'name': 'Garlic Mayo',
                'description': 'Creamy garlic mayo.',
                'price': '1.00',
            },
            {
                'name': 'Local Hot Honey',
                'description': 'Locally produced hot honey.',
                'price': '1.00',
            },
            {
                'name': 'Local Hot Sauce',
                'description': 'Locally produced hot sauce — ask us for available flavours.',
                'price': '1.00',
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with The Crust real menu data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing menu data...')
        MenuItem.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Seeding menu...')
        for cat_data in MENU_DATA:
            category = Category.objects.create(
                name=cat_data['name'],
                slug=slugify(cat_data['name']),
                order=cat_data['order'],
            )
            for item_data in cat_data['items']:
                MenuItem.objects.create(
                    category=category,
                    name=item_data['name'],
                    slug=slugify(item_data['name']),
                    description=item_data.get('description', ''),
                    price=item_data['price'],
                    is_featured=item_data.get('is_featured', False),
                    is_available=True,
                )
        self.stdout.write(self.style.SUCCESS('Real menu seeded successfully!'))