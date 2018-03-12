from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Object

# Create your views here.

class HomePageView(TemplateView):
    # return render(request, 'news/year_archive.html', context)
    template_name = 'index.html'


def get_geojson_objects(request):
    geobjects = serialize('geojson', Object.objects.all())
    return HttpResponse(geobjects, content_type='json')


