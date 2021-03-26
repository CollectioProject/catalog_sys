from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

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
2) Delete database db.sqlite3
3) Create inital migrations and generate database: makemigrations; migrate;
"""


class CommonInfo(models.Model):
    id = models.AutoField(primary_key=True) # not necessary as django adds this to every model, but declared so that it is clear
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    name = models.CharField(max_length=100, help_text='Enter name')
    description = models.TextField(blank=True, help_text='Enter description')
    
    class Meta:
        abstract = True
        ordering = ['-last_modified', 'name'] # '-' reverses order, e.i. newest first
        # ordering = ['name','-last_modified'] # '-' reverses order, e.i. newest first
    

class Catalog (CommonInfo):
    def get_absolute_url(self):
        return reverse('catalog-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Record(CommonInfo):
    my_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE) # Many records to one Catalog. Deletes all records associated with deleted catalog.
    date_start = models.DateField() # TODO - is date range for when aquired or creation? 
    date_end   = models.DateField()

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
    date_start = models.DateField()
    date_end   = models.DateField()
    owner = models.CharField(max_length=100, help_text='Enter owner', blank=True)
    nation = models.CharField(max_length=100, help_text='Enter nation', blank=True)
    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AN', 'Antartica'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('OC', 'Oceania'),
        ('SA', 'South and Central America'),
    ]
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, default='AS')

    class Meta:
        ordering = ['-date_end'] 

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
