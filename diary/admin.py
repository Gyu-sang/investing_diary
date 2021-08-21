from django.contrib import admin
from .models import Corporation, Diary, BuySell, Like, FavoriteCorporation

# Register your models here.
admin.site.register(Corporation)
admin.site.register(Diary)
admin.site.register(BuySell)
admin.site.register(Like)
admin.site.register(FavoriteCorporation)

