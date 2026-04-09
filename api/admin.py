from django.contrib import admin
from .models import Food,Order,Restaurant,UserProfile

admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Restaurant)
admin.site.register(UserProfile)