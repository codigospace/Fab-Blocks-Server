from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True)
    image = forms.ImageField(required=False)  # Agrega el campo de imagen

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'image')  # Incluye 'image'

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso. Por favor, elige otro.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")
        return email
    
    def save(self, *args, **kwargs):
        image = self.cleaned_data.get('image')
        if not image:
            self.instance.image = 'default.jpg'
        super().save(*args, **kwargs)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'image')
