from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from beautifyme.accounts.models import Profile
from beautifyme.accounts.utils import send_welcome_mail

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if not created:
        return

    send_welcome_mail(instance.email)
    Profile.objects.create(user=instance)




