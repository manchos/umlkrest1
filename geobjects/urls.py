from .views import HomePageView
# from django.conf.urls import include
from django.urls import path

from geobjects.views import HomePageView, get_geojson_objects

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('geobjects_data/', get_geojson_objects, name='objects'),
]