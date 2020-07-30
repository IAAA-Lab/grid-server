
from dggs.dggs_utils.dggs_to_tif_utils import DGGSTifUtils
from dggs.dggs_utils.tif_to_dggs_utils import TifDGGSUtils


class TestsShpDGGS:

    def __init__(self):
        self.tif_utils = TifDGGSUtils()
        self.dggs_utils = DGGSTifUtils()

        self.output_file = 'output.tif'
        self.output_file2 = 'output2.tif'

    def remove_files(self):
        import os
        from glob import glob
        for file in glob('./*.shp'):
            os.remove(file)
        for file in glob('./*.dbf'):
            os.remove(file)
        for file in glob('./*.shx'):
            os.remove(file)

    def test_tif_file_from_cell_dataset(self, c_dataset):
        self.dggs_utils.tif_file_from_cell_dataset(c_dataset, self.output_file2)

    def test_cell_dataset_from_tif_file(self, file):
        return self.tif_utils.get_cell_dataset_from_tif_file(file, 'test_id')


    def test_cell_list(self):
        c_dataset = self.test_cell_dataset_from_tif_file(self.output_file)
        c_dataset.print()
        self.test_tif_file_from_cell_dataset(c_dataset)

        c_dataset_2 = self.test_cell_dataset_from_tif_file(self.output_file2)
        c_dataset_2.print()



if __name__ == "__main__":
    tests = TestsShpDGGS()
    tests.test_cell_list()

