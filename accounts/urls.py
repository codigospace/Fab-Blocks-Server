from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register, login, logout, profile

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]