from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favorite/add/url/', views.add_url, name='add_url'),
    path('favorite/add/', views.add_url_detail, name='add_url_detail'),
    path('favorite/edit/url/', views.edit_url, name='edit_url'),
    path('favorite/edit/', views.edit_url_detail, name='edit_url_detail'),
    path('favorite/delete/', views.delete_url, name='delete_url'),
]