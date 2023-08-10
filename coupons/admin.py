from django.contrib import admin
from .models import Coupon
# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_to', 'valid_from', 'discount', 'active']
    list_filter = ['valid_to', 'valid_from', 'active']
    search_fields = ['code']
