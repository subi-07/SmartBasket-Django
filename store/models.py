from decimal import Decimal
from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.CharField(max_length=240, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # Products in the same group can be suggested as cheaper alternatives.
    swap_group = models.CharField(max_length=80, blank=True, help_text="Use same value for similar alternatives.")
    def __str__(self):
        return self.name
    @property
    def low_stock(self):
        return 0 < self.stock <= 5

class Order(models.Model):
    STATUS_CHOICES = [("PLACED", "Placed"), ("PACKING", "Packing"), ("OUT", "Out for delivery"), ("DELIVERED", "Delivered")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grocery_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="PLACED")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    def __str__(self):
        return f"Order #{self.pk} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    @property
    def line_total(self):
        return self.unit_price * self.quantity
