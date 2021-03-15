from django.shortcuts import render
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CreateUserForm


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


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')

    return render(request, 'catalog/login.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/home')

    context = {'form': form}
    return render(request, 'catalog/register.html', context)