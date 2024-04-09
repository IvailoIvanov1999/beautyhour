from django.template.loader import render_to_string
from mailjet_rest import Client
from django.conf import settings


def send_order_created_mail(email, order_id, order_date, order_shipping_address, order_total_price, products_count):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')
    html_content = render_to_string(
        'web/order-completed-email.html',
        {
            'order_id': order_id,
            'order_date': order_date,
            'order_shipping_address': order_shipping_address,
            'order_total_price': order_total_price,
            'products_count': products_count
        })
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "ivailo9998@gmail.com",
                    "Name": "BeautyHour"
                },
                "To": [
                    {
                        "Email": email
                    }
                ],
                "Subject": "Order completed",
                "TextPart": "Thanks for purchase",
                "HtmlPart": html_content
            }
        ]
    }

    result = mailjet.send.create(data=data)
