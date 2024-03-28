from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile, URL, Categorie, Tag
import datetime
from django.utils import timezone

# Create your views here.

def register(request) :
    if request.method == "POST" :
        username =  request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        mail = request.POST["mail"]
        password = request.POST["password"]
        confirm_password = request.POST["cpassword"]
        if username and first_name and last_name and password and confirm_password :
            user = UserProfile.objects.filter(username=username)
            if not user:
                if password == confirm_password :
                    new_user = User.objects.create_user(username=username, password=password,)
                    try:
                        validate_password(password=password, user=new_user)
                    except ValidationError as err:
                        new_user.delete()
                        return render(request, 'registration/register.html', {'messages': err})
                    
                    UserProfile.objects.create(username=username,first_name=first_name,last_name=last_name,e_mail=mail)
                    auth_user = authenticate(request, username=username, password=password)
                    if auth_user is not None:
                        login(request, auth_user)
                        return redirect('dashboard')
                else :
                    return render(request, 'registration/register.html', {'message': 'Password Not Match'})
            else :
                return render(request, 'registration/register.html', {'message': 'Username Already used'})
        else :
            return render(request, 'registration/register.html', {'message': 'Please Complete Registration Form.'})
        
    return render(request, 'registration/register.html', {'message': 'Try Again!'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            return redirect('dashboard')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def pagination(urls, page_number):
    paginator = Paginator(urls, 10)
    try:
        paginated_urls = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_urls = paginator.page(1)
    except EmptyPage:
        paginated_urls = paginator.page(paginator.num_pages)
    return paginated_urls

def dashboard(request):
    urls = URL.objects.filter(user = request.user.id)
    page_number = request.GET.get('page')
    paginated_urls = pagination(urls=urls, page_number=page_number)
    return render(request, 'favlinks/dashboard.html', {
            'urls': paginated_urls,
        })

def add_url_detail(request):
    categories = Categorie.objects.all()
    tags = Tag.objects.all()
    return render(request, 'favlinks/add.html', {
        'categories': categories,
        'tags': tags
        })
    

def add_url(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        categories = request.POST.getlist('categories')
        tags = request.POST.getlist('tags')
        user_profile = UserProfile.objects.get(id = request.user.id)
        new_url = URL.objects.create(title=title,url=url,user=user_profile)
        for categorie in categories:
            cate = Categorie.objects.get(cate_name = categorie)
            new_url.categories.add(cate)
        for tag in tags:
            tag_s = Tag.objects.get(tag_name = tag)
            new_url.tags.add(tag_s)
        new_url.save()
        return redirect('dashboard')
    return render(request, 'favlinks/add.html', {'message': 'Failed'})   

def edit_url_detail(request):
    if request.method == "POST":
        url = URL.objects.get(id = request.POST['edit_url'])
        categories = Categorie.objects.all()
        tags = Tag.objects.all()
        return render(request, 'favlinks/edit.html', {
            'url': url,
            'categories': categories,
            'tags': tags
        })
    return HttpResponseRedirect(reverse("dashboard"))

def edit_url(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if request.method == "POST":
            title = request.POST['title']
            url = request.POST['url']
            categories = request.POST.getlist('categories')
            tags = request.POST.getlist('tags')
            url_update = URL.objects.get(id = request.POST['edit_url_id'])
            url_update.title = title
            url_update.url = url
            for categorie in categories:
                cate = Categorie.objects.get(cate_name = categorie)
                url_update.categories.add(cate)
            for tag in tags:
                tag_s = Tag.objects.get(tag_name = tag)
                url_update.tags.add(tag_s)
            url_update.save()
            return redirect('dashboard')
        else :
            return HttpResponseRedirect(reverse("dashboard"))
            
def delete_url(request):
    url = URL.objects.get(id = request.POST['delete_url_id'])
    url.delete()
    return redirect('dashboard')
            
def index(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else :
        return dashboard(request=request)
    
def category(request):
    categories = Categorie.objects.filter(user = request.user.id)
    return render(request, 'categories/category.html', {
            'categories': categories,
        })
    
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        categories = Categorie.objects.all()
        categories_name = [categorie.cate_name for categorie in categories]
        if name in categories_name:
            return render(request, 'categories/add.html', {
                'message': f'This categorie name "{name}" already used',
            })
        user_profile = UserProfile.objects.get(id = request.user.id)
        new_category = Categorie.objects.create(cate_name=name, user=user_profile)
        new_category.save()
        return redirect('category')
    return HttpResponseRedirect(reverse("dashboard"))

def add_category_detail(request):
    categories = Categorie.objects.all()
    return render(request, 'categories/add.html', {
        'categories': categories,
    })

def edit_category(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if request.method == "POST":
            cate_update = Categorie.objects.get(id = request.POST['cate_id'])
            cate_update.cate_name = request.POST['name']
            cate_update.save()
            return redirect('category')
        else :
            return HttpResponseRedirect(reverse("dashboard"))

def edit_category_detail(request):
    if request.method == "POST":
        cate = Categorie.objects.get(id = request.POST['edit_category'])
        return render(request, 'categories/edit.html', {
            'categories': cate,
        })
    return HttpResponseRedirect(reverse("dashboard"))

def delete_category(request):
    cate =  Categorie.objects.get(id = request.POST['cate_id'])
    cate.delete()
    return redirect('category')

def tag(request):
    tags = Tag.objects.filter(user = request.user.id)
    return render(request, 'tags/tag.html', {
            'tags': tags,
        })

def add_tag(request):
    if request.method == 'POST':
        name = request.POST['name']
        tags = Tag.objects.all()
        tags_name = [tag.tag_name for tag in tags]
        if name in tags_name:
            return render(request, 'tags/add.html', {
                'message': f'This tag name "{name}" already used',
            })
        user_profile = UserProfile.objects.get(id = request.user.id)
        new_tag = Tag.objects.create(tag_name=name, user=user_profile)
        new_tag.save()
        return redirect('tag')
    return HttpResponseRedirect(reverse("dashboard"))

def add_tag_detail(request):
    tags = Tag.objects.all()
    return render(request, 'tags/add.html', {
        'tags': tags,
    })

def edit_tag(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if request.method == "POST":
            tag_update = Tag.objects.get(id = request.POST['tag_id'])
            tag_update.cate_name = request.POST['name']
            tag_update.save()
            return redirect('tag')
        else :
            return HttpResponseRedirect(reverse("dashboard"))

def edit_tag_detail(request):
    if request.method == "POST":
        tag = Tag.objects.get(id = request.POST['tag_id'])
        return render(request, 'tags/edit.html', {
            'tags': tag,
        })
    return HttpResponseRedirect(reverse("dashboard"))

def delete_tag(request):
    tag =  Tag.objects.get(id = request.POST['tag_id'])
    tag.delete()
    return redirect('tag')

def search(request):
    if request.method == "GET":
        title = request.GET['title_search']
        url = request.GET['url_search']
        category = request.GET['category_search']
        tag = request.GET['tag_search']
        date = request.GET['date_search']

        user_profile = UserProfile.objects.get(id = request.user.id)
        urls = URL.objects.filter(user = user_profile)
        if title:
            urls = urls.filter(title__contains = title)
        if url:
            urls = urls.filter(url__contains = url)
        if category:
            cate = Categorie.objects.filter(cate_name__contains=category, user=user_profile)
            urls = urls.filter(categories__in = cate)
        if tag:
            tag = Tag.objects.filter(tag_name__contains=tag, user=user_profile)
            urls = urls.filter(tags__in = tag, user=user_profile)
        if date:
            urls = urls.filter(create_dtm__gte = date)

        page_number = request.GET.get('page')
        paginated_urls = pagination(urls=urls, page_number=page_number)
        return render(request, 'favlinks/dashboard.html', {
                'urls': paginated_urls,
            })
    return redirect('dashboard')