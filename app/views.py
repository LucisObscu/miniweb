from django.shortcuts import render

# Create your views here.

from app.models import *


def clien(request):
    a=Clien.objects.all()
    return render(
        request,
        'app/clien.html',
        {
            'data':a
        }
    )