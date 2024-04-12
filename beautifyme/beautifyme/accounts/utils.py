from django.template.loader import render_to_string
from mailjet_rest import Client
from django.conf import settings


def send_welcome_mail(email):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')
    html_content = render_to_string('accounts/welcome-email.html', {'user_email': email, 'website_url': 'https://beautyhour.azurewebsites.net/'})
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
                "Subject": "Welcome to BeautyHour",
                "TextPart": "Greeting from BeautyHour!",
                "HtmlPart": html_content
            }
        ]
    }

    result = mailjet.send.create(data=data)
