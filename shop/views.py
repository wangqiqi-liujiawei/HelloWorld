from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


# Create your views here.
def produtc_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    html_name = 'shop/product/list.html'
    datas = {'categories': categories, 'products': products, 'category': category}
    return render(request, html_name, datas)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    html_name = 'shop/product/detail.html'
    cartadd = CartAddProductForm()
    datas = {'product': product, 'cartadd': cartadd}
    return render(request, html_name, datas)
