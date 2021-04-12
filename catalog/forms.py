from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['my_catalog', 'acquisition_date', 'creation_date', 'manufacturer', 'condition_rating', 'condition_description', 'name', 'description']


class CreateCatalogForm(ModelForm):
    class Meta:
        model = Catalog
        fields = ['name', 'description']


class CreateProvenanceForm(ModelForm):
    class Meta:
        model = Provenance
        fields = ['record', 'date', 'owner', 'nation']


class CreateManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']


class SearchForm(forms.Form):
    searchString = forms.CharField(max_length=100)
