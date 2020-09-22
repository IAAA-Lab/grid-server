import unittest
from dggs.cellset.boundary import Boundary
from dggs.dataset.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.dataset.data import Data
from dggs.dggs_utils.dggs_to_shp_utils import DGGSShpUtils
from dggs.dggs_utils.shp_to_dggs_utils import ShpDGGSUtils


class TestsShpDGGS(unittest.TestCase):

    def setUp(self):
        self.shp_utils = ShpDGGSUtils()
        self.dggs_utils = DGGSShpUtils()

        self.cells = [CellID('P22220720648'), CellID('P22220720656'), CellID('P22220720657'),
                      CellID('P22220720672'), CellID('P22220720680'), CellID('P22220720681')]
        self.boundary = Boundary(cells=self.cells)
        self.b_dataset = BoundaryDataSet('test_id')
        self.data = Data("data_test")
        self.b_dataset.add(self.boundary, self.data)

        self.output_file = 'output.shp'

    def tearDown(self):
        import os
        from glob import glob
        for file in glob('./*.shp'):
            os.remove(file)
        for file in glob('./*.dbf'):
            os.remove(file)
        for file in glob('./*.shx'):
            os.remove(file)

    def test_cell_list(self):
        self.dggs_utils.shp_file_from_cells(self.cells, self.output_file)
        cells, data = self.shp_utils.get_cells_from_shp_file(self.output_file, True)
        boundary = Boundary(cells=cells)
        assert boundary.boundary_ID.value == self.boundary.boundary_ID.value

    def test_boundary(self):
        self.dggs_utils.shp_file_from_boundary(self.boundary, self.output_file, False)
        boundary, data = self.shp_utils.get_boundary_from_shp_file(self.output_file, True)
        assert boundary.boundary_ID.value == self.boundary.boundary_ID.value

    def test_boundary_dataset(self):
        self.dggs_utils.shp_files_from_boundary_dataset(self.b_dataset, self.output_file, False)
        bds = self.shp_utils.get_boundary_dataset_from_shp_file('./', 'test_id', True, unic_data=True)
        boundary_data = bds.get_boundaries_and_data()
        assert len(boundary_data) == 1
        assert boundary_data[0][0].cells == self.cells


if __name__ == '__main__':
    unittest.main()
