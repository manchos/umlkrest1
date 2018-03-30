import os
from django.contrib.gis.utils import LayerMapping
from .models import Flood

flood_mapping = {
    'ob': 'Ob',
    'river': 'River',
    'riv_sys': 'Riv_sys',
    'riv_in_sys': 'Riv_in_sys',
    'geom': 'MULTIPOLYGON',
}

flood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Flood_zones_poly.shp'))

def run(verbose=True):
    lm = LayerMapping(Flood, flood_shp, flood_mapping, transform=False, encoding='utf8')
    lm.save(strict=True, verbose=verbose)