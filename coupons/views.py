from django.shortcuts import redirect
from .forms import CouponForm
from .models import Coupon
from django.views.decorators.http import require_POST
from django.utils import timezone
# Create your views here.


@require_POST
def coupon_apply(requset):
    now = timezone.now()
    form = CouponForm(requset.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        active=True,
                                        valid_from__lte=now,
                                        valid_to__gte=now)
            print('coupon.id')
            requset.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            print('DoesNotExist coupon.id')
            requset.session['coupon_id'] = None
    return redirect('cart:cart_detail')
