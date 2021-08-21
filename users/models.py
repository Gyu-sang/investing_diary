from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from . managers import UserManager

# Create your models here.

class User(AbstractUser):
    username = None
    first_name = None 
    last_name = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="profiles")
    job = models.CharField(max_length=50)
    bio = models.TextField()
    investingStartedAt = models.DateTimeField(default = timezone.now)
    feedEndAt = models.DateTimeField(default = timezone.now, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
