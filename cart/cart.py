from django.conf import settings
from shop.models import Product
from decimal import Decimal as dec


class Cart(object):
    def __init__(self, request) -> None:
        self.sesion = request.session
        cart = self.sesion.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.sesion[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        # 会话对象它已经被修改 当设置为 True 时，Django 会根据每个请求将会话保存到数据库中。
        self.sesion.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = dec(item['price'])
            item['total_price'] = (item['price']) * item['quantity']
            # 生成器
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(dec(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.sesion[settings.CART_SESSION_ID]
        self.save()
