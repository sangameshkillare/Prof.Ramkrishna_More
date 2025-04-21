from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import DepartmentAdminAccess

@receiver(post_save, sender=DepartmentAdminAccess)
def assign_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='DepartmentAdmin')
        instance.user.groups.add(group)
