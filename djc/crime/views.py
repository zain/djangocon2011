from crime.models import Crime
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse
from django.shortcuts import render
import datetime, json


def map(request):
    return render(request, 'map.html')


def crimes(request):
    min_lat, min_lon, max_lat, max_lon = request.GET['bbox'].split(',')
    bbox = Polygon.from_bbox([min_lon, min_lat, max_lon, max_lat])

    crimes = Crime.objects.filter(date_time__gt=datetime.date(2011, 8, 1)).filter(pt__within=bbox)

    fc = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [crime.pt.x, crime.pt.y],
            },
            'properties': {
                'crime_type': crime.crime_type,
                'date_time': crime.date_time.isoformat(),
                'description': crime.description,
            }
        } for crime in crimes],
    }

    return HttpResponse(json.dumps(fc))
