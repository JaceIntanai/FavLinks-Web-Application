from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favorite/add/', views.add_url, name='add_url'),
    path('favorite/add/form/', views.add_url_detail, name='add_url_detail'),
    path('favorite/edit/', views.edit_url, name='edit_url'),
    path('favorite/edit/form/', views.edit_url_detail, name='edit_url_detail'),
    path('favorite/delete/', views.delete_url, name='delete_url'),
    path('category/', views.category, name='category'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/add/form/', views.add_category_detail, name='add_category_detail'),
    path('category/edit/', views.edit_category, name='edit_category'),
    path('category/edit/form/', views.edit_category_detail, name='edit_category_detail'),
    path('category/delete/', views.delete_category, name='delete_category'),
    path('tag/', views.tag, name='tag'),
    path('tag/add/', views.add_tag, name='add_tag'),
    path('tag/add/form/', views.add_tag_detail, name='add_tag_detail'),
    path('tag/edit/', views.edit_tag, name='edit_tag'),
    path('tag/edit/form/', views.edit_tag_detail, name='edit_tag_detail'),
    path('tag/delete/', views.delete_tag, name='delete_tag'),
    path('search/', views.search, name='search'),
]