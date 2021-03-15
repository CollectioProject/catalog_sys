from typing import Tuple
from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid

# Create your models here.
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
        ordering = ['name','-last_modified'] # '-' reverses order, e.i. newest first

class Catalog (CommonInfo):

    def get_absolute_url(self):
        return reverse('catalog-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.id})'
    

class Record(CommonInfo):
    my_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE) # Many records to one Catalog. Deletes all records associated with deleted catalog.
    

    # Methods
    def get_absolute_url(self):
        return reverse('record-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} ({self.my_catalog})'
    pass
