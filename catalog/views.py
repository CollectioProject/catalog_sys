from django.shortcuts import render
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CreateUserForm
from . filters import RecordFilter

from django.contrib.auth.decorators import login_required


def about(request):
    return render(request, 'catalog/about.html')


def home(request):
    return render(request, 'catalog/home.html')


@login_required(login_url='/login')
def recordList(request, cr):
    records = models.Record.objects.filter(my_catalog=cr)
    provenances = models.Provenance.objects.all()

    context = {
        'records': records,
        'provenances': provenances,
    }
    # render gets the recordlist.html file from the folder in catalog/templates/catalog
    return render(request, 'catalog/recordlist.html', context)


@login_required(login_url='/login')
def search(request):
    catalogs = models.Catalog.objects.all()
    manufacturers = models.Manufacturer.objects.all()

    records = models.Record.objects.all()
    provenances = models.Provenance.objects.all()

    myFilter = RecordFilter(request.GET, queryset=records)
    records = myFilter.qs

    context = {
        'records': records,
        'provenances': provenances,
        'myFilter': myFilter,
        'catalogs': catalogs,
        'manufacturers': manufacturers,
    }
    # render gets the recordlist.html file from the folder in catalog/templates/catalog
    return render(request, 'catalog/recordlist.html', context)



@login_required(login_url='/login')
def catalogList(request):
    if request.user.is_authenticated:
        # catalogs = None
        if request.user.is_superuser:
            catalogs = models.Catalog.objects.all()
        else:
            catalogs = models.Catalog.objects.filter(created_by__exact=request.user)

        context = {'catalogs': catalogs, }
        return render(request, 'catalog/cataloglist.html', context)
    else:
        return HttpResponseRedirect('/login')


def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                messages.info(request, 'Username or password is incorrect!')
                return HttpResponseRedirect('/login')

    return render(request, 'catalog/login.html')


@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/login')


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                print("save")
                return HttpResponseRedirect('/login')

        context = {'form': form}
    return render(request, 'catalog/register.html', context)
