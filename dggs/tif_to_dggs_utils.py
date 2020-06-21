
import rasterio
from numpy import pi
from math import radians, cos, sin, asin, sqrt

from dggs.cell_dataset import CellDataSet
from dggs.data import Data
from dggs.rHealPix import rHEALPix
import os


class TifDGGSUtils:

    def __init__(self, dggs=None):
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def tif_file_treatment(self, file):
        dataset = rasterio.open(file)
        pix0 = dataset.xy(0, 0)
        pix1 = dataset.xy(0, 1)

        #Obtener longitud del lado de un pixel en metros (ya que rasterio me lo da en grados)
        lon1, lat1, lon2, lat2 = map(radians, [pix0[0], pix0[1], pix1[0], pix1[1]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = self.dggs.R_q
        side = c * r

        refinement = self.dggs.refinement_for_area(side ** 2)
        resolution = (pi/2) / (self.dggs.N_side ** refinement)

        # ds = gdal.Warp('rhealpix_aux.tif', file, srcSRS='EPSG:4326',
        #                dstSRS='+proj=rhealpix +lon_0=0 +a=1 +ellps=WGS84 +npole=0 +spole=0 +wktext',
        #                xRes=resolution,
        #                yRes=resolution,
        #                creationOptions="COMPRESS=PAC")

        warp = 'gdalwarp -s_srs EPSG:4326 -t_srs \'+proj=rhealpix +lon_0=0 +a=1 +ellps=WGS84 +npole=0 +spole=0 +wktext\' -tr ' + str(resolution) \
               + ' ' + str(resolution) + ' -co \"COMPRESS=PAC\" ' + file + ' rhealpix_aux.tif'
        os.system(warp)

        dataset_rhealpix = rasterio.open('rhealpix_aux.tif')
        band_rhealpix = dataset_rhealpix.read(1)

        # array = dataset_rhealpix.read()
        # stats = []
        # for band in array:
        #     stats.append({
        #         'min': band.min(),
        #         'mean': band.mean(),
        #         'max': band.max()})
        # print(stats)

        from glob import glob
        for file in glob('./rhealpix_aux.tif'):
            os.remove(file)

        return dataset_rhealpix, band_rhealpix, refinement

    def get_cell_dataset_from_tif_file(self, file, id):
        cds = CellDataSet(id=id)
        dataset, band, refinement = self.tif_file_treatment(file)
        for j in range(dataset.height):
            print(str(j) + "/" + str((dataset.height)))
            for i in range(dataset.width):
                cell_rHealPix_coords = dataset.xy(j, i)
                cell = self.dggs.get_cell_from_projected_point(refinement, cell_rHealPix_coords)
                data = Data(int(band[j, i]))
                cds.add(cell, data)
            if j == 10:
                break

        return cds

    """
    CLI
    """
    def get_cell_dataset_from_tif_file_cli(self, file, id, output_file=None):
        print("CELL DATASET")
        cds = self.get_cell_dataset_from_tif_file(file, id)
        cds_json = cds.toJSON()
        if output_file:
            with open(output_file, 'a') as json_file:
                json_file.write(cds_json)
                print("Saved")
        else:
            print(cds_json)


if __name__ == "__main__":
    import getopt, sys

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "i:o:h"
    long_options = ["input=", "output=", "id="]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    input_file = ''
    output_file = ''
    cds_id = ''

    for current_argument, current_value in arguments:
        if current_argument in ("-i", "--input"):
            input_file = current_value
        elif current_argument in ("-o", "--output"):
            output_file = current_value
        elif current_argument in ("--id"):
            cds_id = current_value
        elif current_argument in ("-h", "--help"):
            print("Displaying help")
            print("-i | --input= -> input GeoTiff ")
            print("-o | --output= -> if you want to save in a file, the output file (.json)")
            print("--id -> Cell Dataset identifier")

    if input_file == '' or cds_id == '':
        print("Error: A file and id is necessary")
        sys.exit(2)

    tif_utils = TifDGGSUtils()
    tif_utils.get_cell_dataset_from_tif_file_cli(input_file, cds_id, output_file=output_file)
