from django.urls import path
from .views import default, index

urlpatterns = [
    path('', default, name='default'),
]
