from django.db import models
from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Order(models.Model):
    first_name = models.CharField(_('first_name'), max_length=50)
    address = models.CharField(_('address'), max_length=250)
    last_name = models.CharField(_('last_name'), max_length=50)
    email = models.EmailField(_('email'))
    postal_code = models.CharField(_('postal_code'), max_length=50)
    city = models.CharField(_('city'), max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=200, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, on_delete=models.SET_NULL, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Ordering {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - (total_cost * (self.discount / Decimal(100)))

    def get_total_cost_after(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return (total_cost * (self.discount / Decimal(100)))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='oder_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
