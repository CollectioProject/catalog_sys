from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CreateUserForm, CreateRecordForm, CreateCatalogForm, SearchForm
from . filters import RecordFilter

from django.contrib.auth.decorators import login_required

from .models import Record


def about(request):
    return render(request, 'catalog/about.html')


def home(request):
    return render(request, 'catalog/home.html')


@login_required(login_url='/login')
def recordList(request, cr):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            records = models.Record.objects.filter(my_catalog__id=cr)
        else:
            records = models.Record.objects.filter(my_catalog__id=cr, my_catalog__created_by=request.user)
        provenances = models.Provenance.objects.all()
        context = {
                'records': records,
                'provenances': provenances,
        }
        # render gets the recordlist.html file from the folder in catalog/templates/catalog
        return render(request, 'catalog/recordlist.html', context)
    else:
        return HttpResponseRedirect('/login')


# @login_required(login_url='/login')
# def simpleSearch(request):
#     if request.method == 'POST':
#         searched = request.POST['searched']
#         records = Record.objects.filter(name__contains=searched)
#         return render(request, 'catalog/recordlist.html', {'searched':searched, 'records':records})
#     else:
#         return render(request, 'catalog/recordlist.html', {})


@login_required(login_url='/login')
def advancedSearch(request):
    catalogs = models.Catalog.objects.all()
    manufacturers = models.Manufacturer.objects.all()

    if request.user.is_superuser:
        records = models.Record.objects.all()
    else:
        records = models.Record.objects.filter(my_catalog__created_by=request.user)
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
                user = form.cleaned_data.get("username")
                messages.success(request, "Account successfully registered for" + user)

                return HttpResponseRedirect('/login')
            else:
                messages.info(request,
                              'Account creation was not successful. Make sure all fields are entered, that your password \n is strong, and that your two password entries match.')
                return HttpResponseRedirect('/register')  # Trying to redirect register page
        context = {'form': form}
    return render(request, 'catalog/register.html', context)


@login_required(login_url='/login')
def createRecord(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/search')

    context = {'form': form,}
    return render(request, 'catalog/create_record.html', context)


@login_required(login_url='/login')
def recordDetail(request, pk):
    records = models.Record.objects.filter(id__exact=pk)
    provenances = models.Provenance.objects.all()
    context = {
        'records': records,
        'provenances': provenances,
    }
    return render(request, 'catalog/record_detail.html', context)


@login_required(login_url='/login')
def updateRecord(request, ur):
    record = Record.objects.get(id=ur)
    form = CreateRecordForm(instance=record)

    if request.method == 'POST':
        form = CreateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('/search')

    context = {
        'form': form,
        'item': record,
    }
    return render(request, 'catalog/update_record.html', context)


@login_required(login_url='/login')
def deleteRecord(request, ur):
    record = Record.objects.get(id=ur)
    if request.method == "POST":
        record.delete()
        return redirect('/search')

    context = {'item': record,}
    return render(request, 'catalog/delete_record.html', context)


@login_required(login_url='/login')
def createCatalog(request):
    form = CreateCatalogForm()

    if request.method == 'POST':
        form = CreateCatalogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/search')

    context = {'form': form,}
    return render(request, 'catalog/create_catalog.html', context)
