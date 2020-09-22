
import unittest
from dggs.cellset.boundary import OptimalBoundary
from dggs.dataset.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.dataset.data import Data

class TestBoundaryDataSet(unittest.TestCase):
    def test_boundary_dataset(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        b_dataset = BoundaryDataSet('id', b_ds)
        self.assertEqual(b_dataset.boundary_data_set, b_ds)


    def test_boundary_dataset_add(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        b_dataset.add(boundary3, data)
        b_ds2 = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        self.assertEqual(b_dataset.boundary_data_set, b_ds2)


    def test_boundary_dataset_add_list(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        boundary4 = OptimalBoundary(cells=[CellID('P33'), CellID('P44')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        b_dataset.add_list([(boundary3, data), (boundary4, data)])
        b_ds2 = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data),
            boundary4.boundary_ID.value: (boundary4, data)
        }
        self.assertEqual(b_dataset.boundary_data_set, b_ds2)


    def test_get_boundaries(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        boundaries = b_dataset.get_boundaries()

        self.assertEqual(boundaries, [boundary1, boundary2, boundary3])


    def test_get_boundaries_and_data(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        boundaries_data = b_dataset.get_boundaries_and_data()

        self.assertEqual(boundaries_data, [(boundary1, data), (boundary2, data), (boundary3, data)])


    def test_get_min_refinement(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        self.assertEqual(b_dataset.get_min_refinement(), 0)


    def test_get_max_refinement(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        self.assertEqual(b_dataset.get_max_refinement(), 5)


    def test_get_boundary_data(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('data')
        data2 = Data('data2')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data2)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        self.assertEqual(b_dataset.get_boundary_data(boundary3.boundary_ID), data2)


    def test_get_boundary_data_list(self):
        boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
        boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
        data = Data('data')
        data2 = Data('data2')

        b_ds = {
            boundary1.boundary_ID.value: (boundary1, data),
            boundary2.boundary_ID.value: (boundary2, data),
            boundary3.boundary_ID.value: (boundary3, data2)
        }
        b_dataset = BoundaryDataSet('id',b_ds)

        self.assertEqual(b_dataset.get_boundary_data_list([boundary1.boundary_ID, boundary3.boundary_ID]), [data, data2])



if __name__ == '__main__':
    unittest.main()
