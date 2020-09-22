import unittest
from dggs.cellset.boundary import OptimalBoundary
from dggs.dataset.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.dataset.cell_dataset import CellDataSet
from dggs.dataset.data import Data


class TestCellDataSet(unittest.TestCase):
    def test_cell_dataset(self):
        cell_data_set = {
            'N01': (CellID('N01'), Data('test')),
            'N02': (CellID('N02'), Data('test')),
            'N03': (CellID('N03'), Data('test'))
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        self.assertEqual(c_dataset.cell_data_set, cell_data_set)

    def test_cell_dataset_add(self):
        cells = [CellID('N01'), CellID('N02'), CellID('N03'), CellID('N04')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        c_dataset.add(cells[3], data)

        self.assertEqual(c_dataset.cells, cells)

    def test_cell_dataset_add_list(self):
        cells = [CellID('N01'), CellID('N02'), CellID('N03'), CellID('N04'), CellID('N05')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        c_dataset.add_list([(cells[3], data), (cells[4], data)])

        self.assertEqual(c_dataset.cells, cells)

    def test_get_cells(self):
        cells = [CellID('N01'), CellID('N02'), CellID('N03')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        self.assertEqual(c_dataset.get_cells(), cells)

    def test_get_cells_and_data(self):
        cells = [CellID('N01'), CellID('N02'), CellID('N03')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        cells_data = c_dataset.get_cells_and_data()

        self.assertEqual(cells_data, [(cells[0], data), (cells[1], data), (cells[2], data)])

    def test_get_min_refinement(self):
        cells = [CellID('P0'), CellID('N02'), CellID('N03')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        self.assertEqual(c_dataset.get_min_refinement(), 1)

    def test_get_max_refinement(self):
        cells = [CellID('P0'), CellID('N02'), CellID('N033')]
        data = Data('test')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
        self.assertEqual(c_dataset.get_max_refinement(), 3)

    def test_get_cell_data(self):
        cells = [CellID('P0'), CellID('N02'), CellID('N033')]
        data = Data('test')
        data2 = Data('test2')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data2)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)

        self.assertEqual(c_dataset.get_cell_data(CellID('N033')), data2)

    def test_get_cell_data_list(self):
        cells = [CellID('P0'), CellID('N02'), CellID('N033')]
        data = Data('test')
        data2 = Data('test2')
        cell_data_set = {
            cells[0].value: (cells[0], data),
            cells[1].value: (cells[1], data),
            cells[2].value: (cells[2], data2)
        }

        c_dataset = CellDataSet('id', cell_data_set=cell_data_set)

        self.assertEqual(c_dataset.get_cell_data_list([cells[0], cells[2]]), [data, data2])


if __name__ == '__main__':
    unittest.main()
