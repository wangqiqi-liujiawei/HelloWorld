from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint


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


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = 'admin/orders/order/detail.html'
    datas = {'order': order}
    return render(request, html, datas)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = 'orders/order/pdf.html'
    datas = {'order': order}
    htmls = render_to_string(html, datas)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=htmls).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
