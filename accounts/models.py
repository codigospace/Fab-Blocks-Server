from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal'),
        ('profesor', 'Profesor'),
    )

    birth_date = models.DateField(null=True, blank=False)
    email = models.EmailField(unique=True)
    image = models.ImageField(default='default.jpg', upload_to='accounts/profile_pics', null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')

    def __str__(self):
        return f'{self.username}'
