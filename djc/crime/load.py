import os
from django.contrib.gis.utils import LayerMapping
from crime.models import Block

block_mapping = {
    'poly' : 'POLYGON',
}

def run():
    lm = LayerMapping(Block, 'data/blocks/tl_2010_06075_tabblock10.shp', block_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save()
