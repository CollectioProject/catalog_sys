from django.shortcuts import render
from . import models

# Create your views here.
post = [
    {
        'id': '1230314',
        'title':'Antique Piece 1',
        'description': 'a nice piece of a chair',
        'created':'January 20, 2021',
        'updated':'January 21, 2021',
    },
    {
        'id': '22222222',
        'title':'Antique Piece 2',
        'description': 'a nice piece of a chair',
        'created':'February 20, 2021',
        'updated':'February 21, 2021',
    }
]


def about(request):
    return render(request, 'catalog/about.html')


def home(request):
    return render(request, 'catalog/home.html')


def catalogList(request):
    posts = models.Record.objects.all()
    context = {
        'posts': posts,
    }

    # render works in such a way that it gets the cat_list.html file from the blog folder in templates.
    return render(request, 'catalog/cataloglist.html', context)


