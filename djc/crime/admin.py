from django.contrib.gis import admin
from crime.models import Block, Crime

class BlockAdmin(admin.OSMGeoAdmin):
    map_template = 'gis/admin/google.html'
    extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAL0km26Ff1JhTQZ8zz5_UJRRRJsJUbtot1GuHKcKo4TPEg7-RbhSq_cjixYTRNfDV1K5E9wfiSuZ5pg']


admin.site.register(Block, BlockAdmin)
admin.site.register(Crime, admin.OSMGeoAdmin)
