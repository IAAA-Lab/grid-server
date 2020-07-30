import gdal
from dggs.dataset.cell_dataset import CellDataSet
from dggs.rHealPix import rHEALPix
from numpy import pi
import numpy
from osgeo import gdal
import os


class DGGSTifUtils:

    def __init__(self, dggs=None):
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def get_row(self, row_list):
        row = ''
        first = True
        for index in row_list:
            if not first:
                row = row + str(index)
            else:
                first = False
        return row

    def orderByCell(self, pair):
        return pair[0].value

    def write_tif(self, raster_data_array, XSize, YSize, resolution, raster_resolution, bbox, output_file):
        # Create gtif file
        driver = gdal.GetDriverByName("GTiff")

        r_output_file = 'rhealpix_' + output_file

        dst_ds = driver.Create(r_output_file,
                               XSize,
                               YSize,
                               1,
                               gdal.GDT_Int16)
        new_array = numpy.array(raster_data_array)

        dst_ds.GetRasterBand(1).WriteArray(new_array)
        dst_ds.GetRasterBand(1).SetNoDataValue(255)
        # setting extension of output raster
        # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
        dst_ds.SetGeoTransform((bbox[0][3][0], resolution, 0.0, bbox[0][3][1], 0.0, -resolution))

        # setting spatial reference of output raster
        srs = 'PROJCS["unnamed",GEOGCS["WGS 84",DATUM["unknown",SPHEROID["WGS84",6378137,298.257223563]],' \
              'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["custom_proj4"],' \
              'EXTENSION["PROJ4","+proj=rhealpix +lon_0=0 +a=1 +ellps=WGS84 +npole=0 +spole=0 +wktext"]]'

        dst_ds.SetProjection(srs)

        # Close output raster dataset
        dst_ds = None

        warp = 'gdalwarp  -t_srs EPSG:4326 -s_srs \'+proj=rhealpix +lon_0=0 +a=1 +ellps=WGS84 +npole=0 +spole=0 ' \
               '+wktext\' -tr ' + str(raster_resolution) \
               + ' ' + str(raster_resolution) + ' -co \"COMPRESS=PAC\" ' + r_output_file + ' ' + output_file
        os.system(warp)

    def tif_file_from_cell_dataset(self, cell_dataset, out_tif):
        raster_dic = {}
        for (cell_id, data) in cell_dataset.get_cells_and_data():
            row = self.get_row(self.dggs.rowcol(cell_id)[0])
            if row in raster_dic:
                data_list = raster_dic.get(row, [])
                data_list.append((cell_id, data))
                raster_dic[row] = data_list
            else:
                raster_dic[row] = [(cell_id, data)]

        keys = list(raster_dic.keys())
        keys.sort()

        raster_array = []
        for key in keys:
            cell_list = raster_dic[key]
            cell_list.sort(key=self.orderByCell)
            raster_array.append(cell_list)

        raster_data_array = []

        XSize = 0
        YSize = 0
        for row in raster_array:
            data_row = []
            XSize = 0
            for (cell_id, data) in row:
                data_row.append(data.content)
                XSize = XSize + 1
            raster_data_array.append(data_row)
            YSize = YSize + 1

        geodetic_coordinates = self.dggs.get_cell_geodetic_coordinates(raster_array[0][0][0])
        ul = geodetic_coordinates[0]
        ur = geodetic_coordinates[1]
        raster_res = abs(ur[0] - ul[0])

        resolution = (pi / 2) / (self.dggs.N_side ** cell_dataset.get_max_refinement())
        bbox = cell_dataset.get_bbox(projected=True)

        self.write_tif(raster_data_array, XSize, YSize, resolution, raster_res, bbox, out_tif)

    def tif_file_from_cell_dataset_cli(self, cell_dataset_file, out_tif):
        with open(cell_dataset_file) as json_file:
            cds = CellDataSet("").fromJSON(json_file, file=True)
            self.tif_file_from_cell_dataset(cds, out_tif)


if __name__ == "__main__":
    import getopt, sys

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "i:o:h"
    long_options = ["input=", "output=", "help"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    input_file = ''
    output_file = ''

    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--input"):
            input_file = current_value
        elif current_argument in ("-o", "--output"):
            output_file = current_value
        elif current_argument in ("-h", "--help"):
            print("Displaying help")
            print("-i | --input= -> input json file (defining a cell dataset) ")
            print("-o | --output= -> output GeoTiff (.tif)")

    if input_file == '' and output_file == '':
        print("Error: input_file, output_file and type are necessary")
        sys.exit(2)

    dggs_utils = DGGSTifUtils()
    dggs_utils.tif_file_from_cell_dataset_cli(input_file, output_file)
