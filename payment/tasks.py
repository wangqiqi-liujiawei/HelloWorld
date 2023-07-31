from celery import shared_task
from django.core.mail import EmailMessage
from orders.models import Order
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My shop - EE Invoice no. {order.id}'
    message = 'Please ,find attached the invoice for your recent purchase'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.email]
    print('发票发送邮件')
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheet = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheet=stylesheet)
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    mail_sent = email.send()
    return mail_sent
