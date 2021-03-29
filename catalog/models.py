from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField, DecimalField
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

"""
Everytime a model is changed in a way that affects the structure of data
    python3 manage.py makemigrations
    python3 manage.py migrate

When creating models register them on admin.py

To reset/clear database
1) Remove all migrations files from within project
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete;
    find . -path "*/migrations/*.pyc"  -delete
2) Delete database: rm db.sqlite3
3) Create inital migrations and generate database: makemigrations; migrate;
4) Create superuser: python manage.py createsuperuser
"""


class CommonInfo(models.Model):
    id = models.AutoField(primary_key=True) 
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)

    name = models.CharField(max_length=100, help_text='Enter name')
    description = models.TextField(blank=True, help_text='Enter description')
    
    class Meta:
        abstract = True
        ordering = ['name', '-updated_at'] # '-' reverses order, e.i. newest first
    
class Catalog (CommonInfo):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('catalog-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Record(CommonInfo):
    my_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE) # Many records to one Catalog. Deletes all records associated with deleted catalog.
    acquisition_date = models.CharField(max_length=100, help_text='Please use the following format: <em>YYYY - YYYY<\em>', blank=True, default='Unknown')
    creation_date = models.CharField(max_length=100, help_text='Please use the following format: <em>YYYY<\em>', blank=True, default='Unknown')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=SET_NULL)

    condition_rating =  DecimalField( 
        help_text='Enter condition rating from 0 to 5',
        default=0, 
        decimal_places=2, 
        max_digits=3, 
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('5'))]
    )
    condition_description = models.TextField(blank=True, help_text='Enter condition description')

    def get_absolute_url(self):
        return reverse('record-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.my_catalog})'


class Provenance (models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.CharField(max_length=100, help_text='Please use the following format: <em>YYYY - YYYY<\em>', blank=True, default='Unknown')
    owner = models.CharField(max_length=100, help_text='Enter Owner', blank=True)
    nation = models.CharField(max_length=100, help_text='Enter Nation', blank=True)

    class Meta:
        #ordering = ['-date'] 
        pass

    def get_absolute_url(self):
        return reverse('provenance-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.record.name}-provenance-{self.id}'


class Manufacturer (models.Model):
    name = models.CharField(max_length=100, help_text='Enter name')
    
    def get_absolute_url(self):
        return reverse('manufacturer-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'
