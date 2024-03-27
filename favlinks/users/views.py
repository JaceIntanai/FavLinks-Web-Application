from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

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
        
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('dashboard')  # Change 'dashboard' to your desired URL name
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def dashboard(request):
    return render(request, 'registration/dashboard.html', {'message': 'Dashboard'})