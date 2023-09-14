from django.contrib.auth.models import Group
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    common_group = Group.objects.get(name='common')
    common_group.user_set.add(user)
