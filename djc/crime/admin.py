from django.contrib.gis import admin
from crime.models import Crime

admin.site.register(Crime, admin.OSMGeoAdmin)
