from django.shortcuts import render
from .models import Region
from django.contrib.gis.geos import GEOSGeometry
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse, Http404

# Create your views here.


def show_genres(request):
    return render(request, "rigions.html", {'genres': Region.objects.all()})


def is_region(slug_region):
    return True if Region.objects.filter(slug_name=slug_region) else False


def region_info(request, slug_region):
    if is_region(slug_region):
        region = Region.objects.filter(slug_name=slug_region)
        # Region.objects.select_related('water_body').select_related('water_body__region')

        return render(request, 'regions/info.html', context={'slug_region': slug_region})
    else:
        raise Http404


class RegionsView(TemplateView):
    # return render(request, 'news/year_archive.html', context)
    template_name = 'index.html'


def get_geojson_objects(request):
    objs = Region.objects.all()
    pnt = GEOSGeometry(objs[0].location)
    print(objs[0].location.coords)
    geobjects = serialize('geojson', objs)
    return HttpResponse(geobjects, content_type='json')
