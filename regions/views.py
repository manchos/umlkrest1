from django.shortcuts import render
from .models import Region

# Create your views here.


def show_genres(request):
    return render(request, "rigions.html", {'genres': Region.objects.all()})
