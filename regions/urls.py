# from .views import HomePageView
# from django.conf.urls import include
from django.urls import path
from .views import region_info
from .views import RegionsView, get_geojson_objects

urlpatterns = [
    path('', RegionsView.as_view(), name='home'),
    # path('geobjects_data/', get_geojson_objects, name='objects'),
    path('<slug:slug_region>/', region_info)
]
