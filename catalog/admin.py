from django.contrib import admin
from .models import Catalog, Record, Provenance, Manufacturer

# Register your models here.
admin.site.register(Record)
admin.site.register(Catalog)
admin.site.register(Provenance)
admin.site.register(Manufacturer)