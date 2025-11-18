from shapely.wkt import loads
from shapely.strtree import STRtree
from typing import List


class AreaCalculator:
    @staticmethod
    def to_hectares(geom):  
        return geom.area / 10_000

class OptimizedOverlapChecker:
    def __init__(self, area_calc=None, min_area_ha=0.0001):
        self.area_calc = area_calc or AreaCalculator()
        self.min_area_ha = min_area_ha
        self.tree = None
        self.geoms = None

    def check_overlap(self, polygon_wkt, wkt_list: List[str], *args):
        # Carregar geometria do polígono base
        poly = loads(polygon_wkt)

        # Criar geometrias válidas, ignorando WKTs inválidos
        valid_geoms = []
        for w in wkt_list:
            try:
                g = loads(w)
                if g is not None:
                    valid_geoms.append(g)
            except:
                continue  # descarta invalidos

        if not valid_geoms:
            return 0

        # Criar índice espacial
        tree = STRtree(valid_geoms)

        # Buscar candidatos 
        candidates = tree.query(poly)

        overlaps = []

        for candidate in candidates:
            # ⚠️ Garantir que o retorno é geometria
            if not hasattr(candidate, "intersects"):
                continue

            if not poly.intersects(candidate):
                continue

            inter = poly.intersection(candidate)
            if inter.is_empty:
                continue

            area_ha = self.area_calc.to_hectares(inter)
            if area_ha >= self.min_area_ha:
                overlaps.append(area_ha)

        return max(overlaps) if overlaps else 0
