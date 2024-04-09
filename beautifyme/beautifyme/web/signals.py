from django.db.models.signals import post_save
from django.dispatch import receiver

from beautifyme.products.models import Order
from beautifyme.web.utils import send_order_created_mail


@receiver(post_save, sender=Order)
def user_order_created(sender, instance, created, **kwargs):
    if created:
        send_order_created_mail(
            instance.user.email,
            instance.id,
            instance.created_at,
            instance.user.profile.address,
            instance.total_price,
            instance.quantity,
        )
