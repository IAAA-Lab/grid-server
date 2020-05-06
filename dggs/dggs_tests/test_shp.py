import fiona
from py_shp import PyShp


def test_cells_from_shp_file(file, refinement):
    cells = PyShp(file).get_cells_from_shp_file(refinement)
    shapes = fiona.open(file)
    for polygon, cell in zip(shapes, cells):
        assert polygon['properties']['id'] == cell.value


if __name__ == "__main__":
    test_cells_from_shp_file("/data/res_8_clipped_lvl_4_zgz_wgs84.shp", 8)
