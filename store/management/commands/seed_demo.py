from django.core.management.base import BaseCommand
from store.models import Category, Product
class Command(BaseCommand):
    help = "Create sample categories and products for local demonstration."
    def handle(self, *args, **options):
        data = {
            "Fruits": [
                ("Banana (6 pcs)", "Fresh bananas for everyday snacks.", "40.00", 30, "fruit"),
                ("Apple (4 pcs)", "Crisp apples.", "120.00", 15, "fruit"),
                ("Guava (4 pcs)", "A budget-friendly seasonal fruit.", "65.00", 20, "fruit"),
            ],
            "Vegetables": [
                ("Tomato (500 g)", "Everyday cooking essential.", "30.00", 40, "veg"),
                ("Carrot (500 g)", "Fresh carrots.", "45.00", 18, "veg"),
                ("Beetroot (500 g)", "A lower-cost alternative for some recipes.", "35.00", 12, "veg"),
            ],
            "Staples": [
                ("Rice (1 kg)", "Daily staple rice.", "68.00", 25, "rice"),
                ("Wheat Flour (1 kg)", "Whole wheat flour.", "52.00", 22, "flour"),
                ("Cooking Oil (1 L)", "Cooking oil bottle.", "145.00", 4, "oil"),
            ],
            "Dairy": [
                ("Milk (500 ml)", "Daily milk packet.", "30.00", 35, "milk"),
                ("Curd (500 g)", "Fresh curd.", "42.00", 10, "curd"),
            ],
        }
        for category_name, products in data.items():
            category, _ = Category.objects.get_or_create(name=category_name, slug=category_name.lower())
            for name, description, price, stock, group in products:
                Product.objects.update_or_create(name=name, defaults={
                    "category": category, "description": description, "price": price,
                    "stock": stock, "is_active": True, "swap_group": group,
                })
        self.stdout.write(self.style.SUCCESS("Demo grocery categories and products created."))
