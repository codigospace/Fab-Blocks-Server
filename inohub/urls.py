from django.urls import path
from . import views

urlpatterns = [
    path('compile/', views.compile, name='compile'),
    path('saveData/', views.saveData, name='save_data'),
    path('uploadFile/', views.upload, name='upload_hex'),
]
