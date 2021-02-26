from django.shortcuts import render
from . import models

from django.forms.models import model_to_dict

# Create your views here.
posts = [
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

# def home(request):
#     return render(request, 'catalogues/home.html', {'title': 'Home'})


def home(request):
    
    posts = models.Record.objects.all()
    context = {
        'posts': posts,
    }
    # context = models.Record.objects.all()
    # context = [result for result in results]

    # context = [{'posts': i} for i in models.Record.objects.all()]

    # if results is not None:
    # context = model_to_dict(results)
    # else:
    #     context = None

    # render works in such a way that it gets the home.html file from the blog folder in templates.
    return render(request, 'catalog/home.html', context )

