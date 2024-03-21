from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'user_type']  # Agrega 'user_type' a list_display
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'image', 'user_type')}),  # Agrega 'user_type' al fieldsets
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'birth_date', 'image', 'user_type', 'password1', 'password2')}),  # Agrega 'user_type' al add_fieldsets
    )

admin.site.register(CustomUser, CustomUserAdmin)
