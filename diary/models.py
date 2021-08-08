from django.db import models
from users.models import Profile
from config import settings

# Create your models here.
class Corporation(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    # logo = models.ImageField(null=True, upload_to='logos')

    def __str__(self):
        return self.name

class Diary(models.Model):
    # user = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    buy = models.ManyToManyField(Corporation, related_name='item_bought', blank=True, null=True)
    sell = models.ManyToManyField(Corporation, related_name='item_sold', blank=True, null=True)


