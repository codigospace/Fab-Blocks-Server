from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def default(request):
    return render(request, 'default.html')

@login_required(login_url="/auth/login/")
def index(request):
    contexto = {
        'title': 'Fab Blocks',
        'version': '0.1',
        'project':'test'
    }
    return render(request, 'index.html', contexto)