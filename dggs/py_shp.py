import fiona
from boundary import Boundary, OptimalBoundary
from rHealPix import rHEALPix


class PyShp:
    """
    Obtaining cells or boundaries of a shapefile in which polygons
    are specified (using coordinates) that represent cells.
    """
    def __init__(self, file, dggs=None):
        self.file = file
        self.shapes = fiona.open(file)
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def get_cell_ID(self, polygon, refinement):
        from geomet import wkt
        polygon_wkt = (wkt.dumps(polygon['geometry']))

        from shapely import wkt
        g = wkt.loads(polygon_wkt)

        return self.dggs.get_cell_from_point(refinement, g.centroid.coords[0])

    def get_cells_from_shp_file(self, refinement):
        cells = []
        for polygon in self.shapes:
            cells.append(self.get_cell_ID(polygon, refinement))
        return cells

    def get_boundary_from_shp_file(self, refinement):
        cells = []
        for polygon in self.shapes:
            cells.append(self.get_cell_ID(polygon, refinement))
        return Boundary(cells=cells)

    def get_optimal_boundary_from_shp_file(self, refinement):
        cells = []
        for polygon in self.shapes:
            cells.append(self.get_cell_ID(polygon, refinement))
        return OptimalBoundary(cells=cells)
