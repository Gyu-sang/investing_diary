from django.db.models.signals import post_save
from django.dispatch import receiver
from diary.models import Diary 
from . models import Profile
from django.utils import timezone


@receiver(post_save, sender=Diary)
def get_feedEndAt(sender, instance, created, **kwargs):
    user = instance.user
    profile = Profile.objects.get(user=user)
    profile.feedEndAt = timezone.now() + timezone.timedelta(days=7)
    profile.save()
    print("profile updated")