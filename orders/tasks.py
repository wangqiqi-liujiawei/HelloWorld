from celery import shared_task
from .models import Order
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\nYour have successfully placed an order.Your order ID is {order.id}'
    from_email = settings.EMAIL_HOST_USER
    print(from_email)
    recipient_list = [order.email]
    print(recipient_list)
    mail_sent = send_mail(subject, message, from_email, recipient_list)
    return mail_sent
