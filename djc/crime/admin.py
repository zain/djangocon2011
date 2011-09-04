from django.contrib.gis import admin
from crime.models import Block, Crime

admin.site.register(Block, admin.OSMGeoAdmin)
admin.site.register(Crime, admin.OSMGeoAdmin)
