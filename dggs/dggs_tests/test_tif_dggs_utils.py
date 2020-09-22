import unittest
from dggs.dggs_utils.dggs_to_tif_utils import DGGSTifUtils
from dggs.dggs_utils.tif_to_dggs_utils import TifDGGSUtils


class TestsTifDGGS(unittest.TestCase):

    def setUp(self):
        self.tif_utils = TifDGGSUtils()
        self.dggs_utils = DGGSTifUtils()

        self.output_file = 'output.tif'
        self.output_file2 = 'output2.tif'

    def tearDown(self):
        import os
        from glob import glob
        for file in glob('./*.tif'):
            os.remove(file)

    def test_cell_list(self):
        c_dataset = self.tif_utils.get_cell_dataset_from_tif_file(self.output_file, 'test_id')
        c_dataset.print()
        self.dggs_utils.tif_file_from_cell_dataset(c_dataset, self.output_file2)

        c_dataset_2 = self.tif_utils.get_cell_dataset_from_tif_file(self.output_file2, 'test_id')
        c_dataset_2.print()


if __name__ == '__main__':
    unittest.main()
