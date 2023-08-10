from .models import Product
# from shop.models import Product
from django.conf import settings
import redis


# 推荐引擎算法
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def product_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    # 将
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_product_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_ids[0]), start=0, end=-1, desc=True)[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            print(keys)
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))


# if __name__ == '__main__':
#     r = Recommender()
#     black = Product.objects.get(translations__name='Black Tea')
#     red = Product.objects.get(translations__name='Red Tea')
#     green = Product.objects.get(translations__name='Green Tea')
#     white = Product.objects.get(translations__name='White Tea')
#     print(black, red, green, white)
#     r.product_bought([black, red])
#     r.product_bought([black, green])
#     r.product_bought([red, black, white])
#     r.product_bought([green, white])
#     r.product_bought([black, white])
#     r.product_bought([red, green])
#     r.suggest_product_for([black])
#     r.suggest_product_for([red])
#     r.suggest_product_for([green])
#     r.suggest_product_for([white])

#     r.suggest_product_for([black,red])
#     r.suggest_product_for([green,red])
#     r.suggest_product_for([white,black])
