from django.contrib import admin
from .models import UserProfile,URL,Categorie,Tag
# Register your models here.

class userList(admin.ModelAdmin):
    list_user_display = ("username","first_name","last_name","e_mail","create_dtm")

class urlList(admin.ModelAdmin):
    list_url_display = ("title","url","categories","tags","create_dtm")

class categoryList(admin.ModelAdmin):
    list_cate_display = ("name")

class tagList(admin.ModelAdmin):
    list_tag_display = ("name")

admin.site.register(UserProfile, userList)
admin.site.register(URL, urlList)
admin.site.register(Categorie, categoryList)
admin.site.register(Tag, tagList)