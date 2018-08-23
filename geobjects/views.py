from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Object
from django.contrib.gis.geos import GEOSGeometry

import json

# Create your views here.

class HomePageView(TemplateView):
    # return render(request, 'news/year_archive.html', context)
    template_name = 'index.html'


def get_geojson_objects(request):
    objs = Object.objects.all()
    pnt = GEOSGeometry(objs[0].location)
    print(objs[0].location.coords)
    geobjects = serialize('geojson', objs)
    return HttpResponse(geobjects, content_type='json')


