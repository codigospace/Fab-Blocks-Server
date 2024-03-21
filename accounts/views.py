from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un error al registrarse. Por favor, corrige los errores a continuación.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form, 'errors': form.errors})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('fabblocks')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')

@login_required(login_url="/auth/login/")
def profile(request):
    return render(request, 'user_profile.html', {'user': request.user})