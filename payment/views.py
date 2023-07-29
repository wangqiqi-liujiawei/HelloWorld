from django.shortcuts import render, redirect, get_object_or_404
import braintree
from orders.models import Order
from django.conf import settings


# 支付网关
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


# Create your views here.
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        # 结算购物车
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:cancled')
    else:
        client_token = gateway.client_token.generate()
        html = 'payment/process.html'
        datas = {'order': order, 'client_token': client_token}
        return render(request, html, datas)


def payment_done(request):
    html = 'payment/done.html'
    return render(request, html)


def payment_cancled(request):
    html = 'payment/cancled.html'
    return render(request, html)