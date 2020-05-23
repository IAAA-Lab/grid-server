import json
from gdal import ogr

from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class DGGSShpUtils:
    """

    """

    def __init__(self, dggs=None):
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def create_polygon(self, coords):
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for coord in coords:
            ring.AddPoint(coord[0], coord[1])

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        return poly.ExportToWkt()

    def write_shapefile(self, cells, out_shp, data=False):

        driver = ogr.GetDriverByName('Esri Shapefile')
        ds = driver.CreateDataSource(out_shp)
        layer = ds.CreateLayer('', None, ogr.wkbPolygon)

        layer.CreateField(ogr.FieldDefn('id', ogr.OFTString))
        if data:
            layer.CreateField(ogr.FieldDefn('data', ogr.OFSTJSON))
        defn = layer.GetLayerDefn()

        for cell in cells:
            feat = ogr.Feature(defn)
            feat.SetField('id', cell['id'])

            geom = ogr.CreateGeometryFromWkt(cell['cell_poly'])
            feat.SetGeometry(geom)

            if data:
                if cell['id'] in cell['data']:
                    feat.SetField('data', json.dumps(cell['data'][cell['id']]))
                else:
                    feat.SetField('data', json.dumps(cell['data']))
            layer.CreateFeature(feat)

        feat = geom = None  # destroy these
        ds = layer = feat = geom = None

    def shp_file_from_cells(self, cells, out_shp, data=None):
        cell_list = []
        for cell in cells:
            cells_coords = self.dggs.get_cell_geodetic_coordinates(cell)
            coords = [cells_coords[0], cells_coords[1], cells_coords[3], cells_coords[2], cells_coords[0]]
            cell_poly = self.create_polygon(coords)
            if data is not None:
                cell = {
                    'id': cell.value,
                    'cell_poly': cell_poly,
                    'data': data.content
                }
            else:
                cell = {
                    'id': cell.value,
                    'cell_poly': cell_poly,
                }
            cell_list.append(cell)

        if data is not None:
            self.write_shapefile(cell_list, out_shp, data=True)
        else:
            self.write_shapefile(cell_list, out_shp, data=False)

    def shp_file_from_boundary(self, boundary, out_shp, bbox, data=None):
        cell_list = []
        if not bbox:
            for cell in boundary.cells:
                cells_coords = self.dggs.get_cell_geodetic_coordinates(cell)
                coords = [cells_coords[0], cells_coords[1], cells_coords[3], cells_coords[2], cells_coords[0]]
                cell_poly = self.create_polygon(coords)
                if data is not None:
                    cell = {
                        'id': cell.value,
                        'cell_poly': cell_poly,
                        'data': data.content
                    }
                else:
                    cell = {
                        'id': cell.value,
                        'cell_poly': cell_poly,
                    }
                cell_list.append(cell)
        else:
            coords = boundary.get_bbox()
            cell_poly = self.create_polygon(coords[0])
            if data is not None:
                cell = {
                    'id': boundary.boundary_ID.value,
                    'cell_poly': cell_poly,
                    'data': data.content
                }
            else:
                cell = {
                    'id': boundary.boundary_ID.value,
                    'cell_poly': cell_poly,
                }
            cell_list.append(cell)

        if data is not None:
            self.write_shapefile(cell_list, out_shp, data=True)
        else:
            self.write_shapefile(cell_list, out_shp, data=False)

    def shp_files_from_boundary_dataset(self, boundary_dataset, bbox, out_shp):
        index = 0
        for (boundary, data) in boundary_dataset.get_boundaries_and_data():
            cell_list = []
            if not bbox:
                for cell in boundary.cells:
                    cells_coords = self.dggs.get_cell_geodetic_coordinates(cell)
                    coords = [cells_coords[0], cells_coords[1], cells_coords[3], cells_coords[2], cells_coords[0]]
                    cell_poly = self.create_polygon(coords)
                    cell = {
                        'id': cell.value,
                        'cell_poly': cell_poly,
                        'data': data.content
                    }
                    cell_list.append(cell)
            else:
                coords = boundary.get_bbox()
                cell_poly = self.create_polygon(coords[0])
                cell = {
                    'id': boundary.boundary_ID.value,
                    'cell_poly': cell_poly,
                    'data': data.content
                }
                cell_list.append(cell)
            self.write_shapefile(cell_list, str(index) + '_' + out_shp, data=True)
            index = index + 1


    def shp_file_from_boundary_cli(self, boundary_file, out_shp, bbox):
        with open(boundary_file) as json_file:
            boundary = json.load(json_file)
            self.shp_file_from_boundary(Boundary(boundary_ID=BoundaryID(boundary['boundary'])), out_shp, bbox,
                                        data=Data(boundary['data']))

    def shp_files_from_boundary_dataset_cli(self, boundary_dataset_file, out_shp, bbox):
        with open(boundary_dataset_file) as json_file:
            boundary_dataset_json = json.load(json_file)
            bds = BoundaryDataSet("").fromJSON(boundary_dataset_json)
            self.shp_files_from_boundary_dataset(bds, out_shp, bbox)


if __name__ == "__main__":
    import getopt, sys

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "i:o:t:hb"
    long_options = ["input=", "output=", "type=", "bbox","help"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    input_file = ''
    output_file = ''
    type = '-1'
    bbox = False

    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--input"):
            input_file = current_value
        elif current_argument in ("-o", "--output"):
            output_file = current_value
        elif current_argument in ("-t", "--type"):
            type = current_value
        elif current_argument in ("-b", "--bbox"):
            bbox = True
        elif current_argument in ("-h", "--help"):
            print("Displaying help")
            print("-i | --input= -> input json file (defining a boundary or a boundary dataset) ")
            print("-t | --type= -> 0 if file defines a boundary or  1 if defines a boundary dataset")
            print("-o | --output= -> output shapefile (.shp)")
            print("-b | --bbox -> bbox of the boundary instead of the cells it is formed by")

    if input_file == '' and output_file == '' and type == '-1':
        print("Error: input_file, output_file and type are necessary")
        sys.exit(2)

    dggs_utils = DGGSShpUtils()
    if type == '0':
        dggs_utils.shp_file_from_boundary_cli(input_file, output_file, bbox)
    elif type == '1':
        dggs_utils.shp_files_from_boundary_dataset_cli(input_file, output_file, bbox)
    else:
        print("-t | --type= -> 0 if file defines a boundary or  1 if defines a boundary dataset")
        sys.exit(2)
