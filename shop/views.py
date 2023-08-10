from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


# Create your views here.
def produtc_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    language = request.LANGUAGE_CODE
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        products = products.filter(category=category)
    html_name = 'shop/product/list.html'
    datas = {'categories': categories, 'products': products, 'category': category}
    return render(request, html_name, datas)


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id, translations__language_code=language, translations__slug=slug, available=True)
    html_name = 'shop/product/detail.html'
    cartadd = CartAddProductForm()
    r = Recommender()
    recommender_product = r.suggest_product_for([product], 4)
    # for p in recommender_product:
    #     print(p.get_absolute_url())
    datas = {'product': product, 'cartadd': cartadd, 'recommender_product': recommender_product}
    return render(request, html_name, datas)
