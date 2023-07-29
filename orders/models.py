from django.db import models
from shop.models import Product


# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    postal_code = models.CharField(max_length=50)
    city = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Ordering {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='oder_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
