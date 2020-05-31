import json
import fiona

from dggs.boundary import Boundary, OptimalBoundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class ShpDGGSUtils:
    """

    """

    def __init__(self, dggs=None):
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def get_cell_ID(self, polygon, refinement):
        from geomet import wkt
        polygon_wkt = (wkt.dumps(polygon['geometry']))

        from shapely import wkt
        g = wkt.loads(polygon_wkt)

        return self.dggs.get_cell_from_point(refinement, g.centroid.coords[0])

    def get_cells_from_shp_file(self, file, with_ids, refinement=None, unic_data=False):
        shapes = fiona.open(file)
        cells = []
        data = []
        for polygon in shapes:
            if with_ids:
                cells.append(CellID(polygon['properties']['id']))
            else:
                assert refinement is not None
                cells.append(self.get_cell_ID(polygon, refinement))

            if 'data' in polygon['properties']:
                data.append(CellID(polygon['properties']['data']))
            else:
                data.append(CellID(polygon['properties']))
        return cells, data

    def get_boundary_from_shp_file(self, file, with_ids, refinement=None, unic_data=False):
        shapes = fiona.open(file)
        cells = []
        data = {}
        first = True
        for polygon in shapes:
            if with_ids:
                cells.append(CellID(polygon['properties']['id']))
            else:
                assert refinement is not None
                cells.append(self.get_cell_ID(polygon, int(refinement)))

            if not unic_data:
                if 'data' in polygon['properties']:
                    data[polygon['properties']['id']] = polygon['properties']['data']
                else:
                    data[polygon['properties']['id']] = polygon['properties']
            elif unic_data and first:
                if 'data' in polygon['properties']:
                    data = polygon['properties']['data']
                else:
                    data = polygon['properties']
        return Boundary(cells=cells), Data(data)

    def get_optimal_boundary_from_shp_file(self, file, with_ids, refinement=None, unic_data=False):
        shapes = fiona.open(file)
        cells = []
        data = {}
        first = True
        for polygon in shapes:
            if with_ids:
                cells.append(CellID(polygon['properties']['id']))
            else:
                assert refinement is not None
                cells.append(self.get_cell_ID(polygon, int(refinement)))

            if not unic_data:
                if 'data' in polygon['properties']:
                    data[polygon['properties']['id']] = polygon['properties']['data']
                else:
                    data[polygon['properties']['id']] = polygon['properties']
            elif unic_data and first:
                if 'data' in polygon['properties']:
                    data = polygon['properties']['data']
                else:
                    data = polygon['properties']
        return OptimalBoundary(cells=cells), Data(data)

    def get_boundary_dataset_from_shp_file(self, dir, id, with_ids, refinement=None, unic_data=False):
        import os
        import glob
        os.chdir(dir)
        boundaries = []
        for file in glob.glob('*.shp'):
            boundaries.append(fiona.open(file))

        bds = BoundaryDataSet(id=id)
        for boundary in boundaries:
            data = {}
            boundary_id = ''
            first = True
            for polygon in boundary:
                if with_ids:
                    boundary_id = boundary_id + polygon['properties']['id']
                else:
                    assert refinement is not None
                    cell = self.get_cell_ID(polygon, int(refinement))
                    boundary_id = boundary_id + cell.value

                if not unic_data:
                    if 'data' in polygon['properties']:
                        data[polygon['properties']['id']] = polygon['properties']['data']
                    else:
                        data[polygon['properties']['id']] = polygon['properties']
                elif unic_data and first:
                    if 'data' in polygon['properties']:
                        data = polygon['properties']['data']
                    else:
                        data = polygon['properties']
            bds.add(boundary=Boundary(boundary_ID=BoundaryID(boundary_id)), data=Data(data))

        return bds

    """
    CLI
    """
    def get_boundary_dataset_from_shp_file_cli(self, dir, id, with_ids, refinement=None, output_file=None,
                                               optimal=False):
        print("BOUNDARY DATASET")
        bds = self.get_boundary_dataset_from_shp_file(dir, id, with_ids, refinement=refinement)
        bds_json = bds.toJSON(optimal)
        if output_file:
            with open(output_file, 'a') as json_file:
                json_file.write(bds_json)
                print("Saved")
        else:
            print(bds_json)

    def get_boundary_from_shp_file_cli(self, file, with_ids, refinement=None, output_file=None, optimal=False):
        print("BOUNDARY")
        if optimal:
            boundary, data = self.get_optimal_boundary_from_shp_file(file, with_ids, refinement=refinement)
            boundary = {
                'AUID': boundary.boundary_ID.value,
                'boundary': boundary.AUID_to_ID(),
                'data': data.content
            }
        else:
            boundary, data = self.get_boundary_from_shp_file(file, with_ids, refinement=refinement)

            boundary = {
                'boundary': boundary.boundary_ID.value,
                'data': data.content
            }
        boundary_json = json.dumps(boundary)

        if output_file:
            with open(output_file, 'a') as json_file:
                json_file.write(boundary_json)
                print("Saved")
        else:
            print(boundary_json)


if __name__ == "__main__":
    import getopt, sys

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "f:d:r:s:ho"
    long_options = ["file=", "dir=", "id=", "with_ids", "refinement=", "save=", "help", "optimal="]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    file = ''
    dir = ''
    with_ids = False
    refinement = 0
    save = False
    output_file = None
    bds_id = ''
    optimal = False

    for current_argument, current_value in arguments:
        if current_argument in ("-f", "--file"):
            file = current_value
        elif current_argument in ("-d", "--dir"):
            dir = current_value
        elif current_argument in ("--id"):
            bds_id = current_value
        elif current_argument in ("-r", "--refinement"):
            refinement = current_value
        elif current_argument in ("--with_ids"):
            with_ids = True
        elif current_argument in ("-s", "--save"):
            save = True
            output_file = current_value
        elif current_argument in ("-o", "--optimal"):
            optimal = True
        elif current_argument in ("-h", "--help"):
            print("Displaying help")
            print("-f | --file= -> input shapefile (if you want to get a boundary)")
            print("-d | --dir= -> directory with shapefiles (if you want to get a boundary dataset)")
            print("--id -> Boundary Dataset identifier")
            print(
                "--with_ids -> if in the shapefile there is an id property that indicates the identifier of the cells")
            print("-r | --refinement= -> level of refinement if cell identifiers are to be calculated")
            print("-s | --save= -> if you want to save in a file, the output file (.json)")
            print("-o | --optimal= -> include AUID (Optimal Boundary)")

    if (file == '' and dir == '') or (file != '' and dir != ''):
        print("Error: A file or directory is necessary")
        sys.exit(2)

    shp_utils = ShpDGGSUtils()
    if dir == '':

        if with_ids:
            shp_utils.get_boundary_from_shp_file_cli(file, with_ids, output_file=output_file, optimal=optimal)
        else:
            shp_utils.get_boundary_from_shp_file_cli(file, with_ids, refinement=refinement,
                                                     output_file=output_file, optimal=optimal)
    else:
        if bds_id == '':
            print("Error: A Boundary Dataset identifier is necessary")
            sys.exit(2)
        if with_ids:
            shp_utils.get_boundary_dataset_from_shp_file_cli(dir, bds_id, with_ids, output_file=output_file,
                                                             optimal=optimal)
        else:
            shp_utils.get_boundary_dataset_from_shp_file_cli(dir, bds_id, with_ids, refinement=refinement,
                                                             output_file=output_file, optimal=optimal)
