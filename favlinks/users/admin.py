from django.contrib import admin
from .models import UserProfile
# Register your models here.

class userList(admin.ModelAdmin):
    list_display = ("username","first_name","last_name","e_mail","create_dtm")

admin.site.register(UserProfile, userList)