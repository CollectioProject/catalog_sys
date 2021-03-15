from django.contrib import admin
from .models import Catalog, Record

# Register your models here.
admin.site.register(Record)
admin.site.register(Catalog)