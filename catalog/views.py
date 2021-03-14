from django.shortcuts import render
from . import models

def about(request):
    return render(request, 'catalog/about.html')


def home(request):
    return render(request, 'catalog/home.html')


def catalogList(request):
    posts = models.Record.objects.all()
    context = {
        'posts': posts,
    }
    # render gets the cataloglist.html file from the folder in catalog/templates/catalog
    return render(request, 'catalog/cataloglist.html', context)