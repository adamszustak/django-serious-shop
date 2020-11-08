from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import weasyprint
from conf.celery import app
from lib.models import CompanyInfo
from orders.models import Order


@app.task
def order_confirmation(order_id, status, path):
    order = Order.objects.get(id=order_id)
    company = CompanyInfo.objects.latest("id")
    subject = f"Order nr. {order.id}"
    email_from = settings.EMAIL
    email_to = order.get_email
    if status == "paid":
        message = (
            f"Dear {order.shipping_address.first_name},\n\n"
            f"You have successfully placed an order."
            f"Your order ID is {order.id}."
            "Please, find attached the invoice for your recent purchase."
        )
    else:
        message = (
            f"Dear {order.shipping_address.first_name},\n\n"
            f"You have successfully placed an order but it has not been paid. Try again now!"
            f"Your order ID is {order.id}."
        )
    email = EmailMessage(subject, message, email_from, [email_to])
    html = render_to_string("pdf.html", {"order": order, "company": company})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + "/css/pdf.css")]
    weasyprint.HTML(string=html, base_url=path).write_pdf(out, stylesheets=stylesheets)
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
    email.send()


# on WIN10: poetry run celery -A conf worker --pool=solo -l INFO
