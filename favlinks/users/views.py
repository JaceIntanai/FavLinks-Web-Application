from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, URL, Categorie, Tag

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

def dashboard(request):
    urls = URL.objects.filter(user = request.user.id)
    for url in urls:
        print(url.categories.all())
    categories = url.categories.all()
    categories_show = ''
    for i, cate in enumerate(categories):
        if i != len(categories) -1 :
            categories_show += str(cate) + ','
        else:
            categories_show += str(cate)
    tags = url.tags.all()
    tags_show = ''
    for i, tag in enumerate(tags):
        if i != len(tags) -1 :
            tags_show += str(tag) + ','
        else:
            tags_show += str(tag)
    return render(request, 'favlinks/dashboard.html', {
        'message': 'Dashboard',
        'urls': urls,
        'categories': categories_show,
        'tags': tags_show,
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
        print(user_profile)
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
        print(request.POST['edit_url'])
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
    
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_category = Categorie.objects.create(cate_name=name)
        new_category.save()
        return redirect('dashboard')
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
            return redirect('dashboard')
        else :
            return HttpResponseRedirect(reverse("dashboard"))

def edit_category_detail(request):
    if request.method == "POST":
        cate = Categorie.objects.get(id = request.POST['cate_id'])
        return render(request, 'categories/edit.html', {
            'categories': cate,
        })
    return HttpResponseRedirect(reverse("dashboard"))

def delete_category(request):
    cate =  Categorie.objects.get(id = request.POST['cate_id'])
    cate.delete()
    return redirect('dashboard')

def add_tag(request):
    if request.method == 'POST':
        name = request.POST['name']
        new_tag = Tag.objects.create(tag_name=name)
        new_tag.save()
        return redirect('dashboard')
    return HttpResponseRedirect(reverse("dashboard"))

def add_tag_detail(request):
    tags = Tag.objects.all()
    return render(request, 'tags/add.html', {
        'categories': tags,
    })

def edit_tag(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    else :
        if request.method == "POST":
            tag_update = Tag.objects.get(id = request.POST['tag_id'])
            tag_update.cate_name = request.POST['name']
            tag_update.save()
            return redirect('dashboard')
        else :
            return HttpResponseRedirect(reverse("dashboard"))

def edit_tag_detail(request):
    if request.method == "POST":
        tag = Tag.objects.get(id = request.POST['tag_id'])
        return render(request, 'categories/edit.html', {
            'tags': tag,
        })
    return HttpResponseRedirect(reverse("dashboard"))

def delete_category(request):
    tag =  Tag.objects.get(id = request.POST['tag_id'])
    tag.delete()
    return redirect('dashboard')