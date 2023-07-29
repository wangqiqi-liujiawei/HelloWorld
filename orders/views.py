from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 生成新的订单但
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         price=item['price'])
            cart.clear()
            # 发送邮件
            order_created.delay(order.id)
            # 对购物车进行结算
            request.session['order_id'] = order.id
            # 输入信用卡信息并结算
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    html = 'orders/order/create.html'
    datas = {'form': form, 'cart': cart}
    return render(request, html, datas)
