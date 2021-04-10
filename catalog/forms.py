from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = '__all__'


class CreateCatalogForm(ModelForm):
    class Meta:
        model = Catalog
        fields = '__all__'

class CreateProvenanceForm(ModelForm):
    class Meta:
        model = Provenance
        fields = '__all__'

class CreateManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'
