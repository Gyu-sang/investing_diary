from django.db import models
from users.models import Profile
from config import settings
from django.utils import timezone

# Create your models here.

class TimeStampedModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class Corporation(TimeStampedModel):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, through='FavoriteCorporation')   
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="logos")

    def __str__(self):
        return self.name


class Diary(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    corporation = models.ManyToManyField(Corporation, blank=True, null=True, through='BuySell')
    interestedUser = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interested', blank=True, null=True, through='Like')


class BuySell(TimeStampedModel):
    choices = [
        ('buy', '매수'),
        ('sell', '매도')
    ]
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    category = models.CharField(max_length=50, choices = choices)


class Like(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)   

    class Meta:
        unique_together = ['user', 'diary']


class FavoriteCorporation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'corporation']