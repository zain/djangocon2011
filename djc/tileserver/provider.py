from djc.crime.models import Block, Crime
from django.contrib.gis.geos import Point, Polygon
from PIL import Image, ImageDraw
import ModestMaps


START_COLOR = (90, 75, 40)
END_COLOR = (0, 100, 40)
HEATMAP_MIN = 5
HEATMAP_MAX = 15


class CrimeHeatmapProvider:
    def __init__(self, layer, *args, **kwargs):
        self.layer = layer
        self.provider = ModestMaps.OpenStreetMap.Provider()

    def renderArea(self, width, height, srs, xmin, ymin, xmax, ymax, zoom):
        nw = self.layer.projection.projLocation(ModestMaps.Core.Point(xmin, ymin))
        se = self.layer.projection.projLocation(ModestMaps.Core.Point(xmax, ymax))
        max_lat = max(nw.lat, se.lat)
        min_lat = min(nw.lat, se.lat)
        max_lon = max(nw.lon, se.lon)
        min_lon = min(nw.lon, se.lon)

        bound1 = ModestMaps.Geo.Location(min_lat, min_lon)
        bound2 = ModestMaps.Geo.Location(max_lat, max_lon)
        mmap = ModestMaps.mapByExtentZoom(self.provider, bound1, bound2, zoom)

        pil_map = Image.new("RGBA", (width, height), (255,255,255, 0))
        pil_draw = ImageDraw.Draw(pil_map)

        bbox = Polygon.from_bbox((min_lon, min_lat, max_lon, max_lat))

        for block in Block.objects.filter(poly__intersects=bbox):

            # shape
            locs = []
            for c in block.poly.coords[0]:
                pt = ModestMaps.Geo.Location(c[1], c[0])
                loc = mmap.locationPoint(pt)
                locs.append((loc.x, loc.y))
            
            # color
            count = Crime.objects.filter(pt__within=block.poly).count()

            if count <= HEATMAP_MIN:
                h, s, l = START_COLOR
            elif count >= HEATMAP_MAX:
                h, s, l = END_COLOR
            else:
                scale = float(count - HEATMAP_MIN) / float(HEATMAP_MAX - HEATMAP_MIN)
                
                # scale all channels linearly between START_COLOR and END_COLOR
                h, s, l = [int(scale*(end-start) + start)
                                    for start, end in zip(START_COLOR, END_COLOR)]

            pil_draw.polygon(locs, fill="hsl(%s, %s%%, %s%%)" % (h, s, l), outline="rgb(255, 255, 255)")
        
        return pil_map
