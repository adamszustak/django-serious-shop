from django.conf import settings
from django.core.mail import send_mail

from conf.celery import app
from orders.models import Order


@app.task
def order_created(order_id, status):
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    email_from = settings.EMAIL
    email_to = order.get_email
    if status == "paid":
        message = (
            f"Dear {order.shipping_address.first_name},\n\n"
            f"You have successfully placed an order."
            f"Your order ID is {order.id}."
        )
    else:
        message = (
            f"Dear {order.shipping_address.first_name},\n\n"
            f"You have successfully placed an order but it has not been paid. Try again now!"
            f"Your order ID is {order.id}."
        )
    mail_sent = send_mail(subject, message, email_from, [email_to])
    return mail_sent


# on WIN10: poetry run celery -A conf worker --pool=solo -l INFO
