from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid

# Create your models here.
"""
Everytime a model is changed in a way that affects the structure of data
Run:
python3 manage.py makemigrations
python3 manage.py migrate
"""

class Record(models.Model):

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='The Unique ID of record')
    title = models.CharField(max_length=200, help_text='Enter name/title of object')
    description = models.TextField(null=True,blank=True, help_text='Enter a short description of the object on record')
    created = models.DateField(auto_now_add=True, help_text='Date of initial record creation')
    updated = models.DateField(auto_now=True)

    # Metadata
    class Meta:
        ordering = ['updated']

    # Methods
    def get_absolute_url(self):
        return reverse('record-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title} ({self.id})'
    pass
