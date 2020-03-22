from boundary import OptimalBoundary
from boundary_dataset import BoundaryDataSet
from cell_ID import CellID
from data import Data


def test_boundary_dataset():
    boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
    boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
    boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
    data = Data('', '')

    b_ds = {
        boundary1.boundary_ID.value: (boundary1, data),
        boundary2.boundary_ID.value: (boundary2, data),
        boundary3.boundary_ID.value: (boundary3, data)
    }
    b_dataset = BoundaryDataSet(b_ds)
    assert b_dataset.boundary_data_set == b_ds


def test_boundary_dataset_add():
    boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
    boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
    boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
    data = Data('', '')

    b_ds = {
        boundary1.boundary_ID.value: (boundary1, data),
        boundary2.boundary_ID.value: (boundary2, data),
    }
    b_dataset = BoundaryDataSet(b_ds)

    b_dataset.add(boundary3, data)
    b_ds2 = {
        boundary1.boundary_ID.value: (boundary1, data),
        boundary2.boundary_ID.value: (boundary2, data),
        boundary3.boundary_ID.value: (boundary3, data)
    }
    assert b_dataset.boundary_data_set == b_ds2


def test_boundary_dataset_get_boundary_data():
    boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
    boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
    boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
    data = Data('t', 'data')
    data2 = Data('t', 'data2')

    b_ds = {
        boundary1.boundary_ID.value: (boundary1, data),
        boundary2.boundary_ID.value: (boundary2, data),
        boundary3.boundary_ID.value: (boundary3, data2)
    }
    b_dataset = BoundaryDataSet(b_ds)

    assert b_dataset.get_boundary_data(boundary3.boundary_ID) == data2


def test_boundary_dataset_get_boundary_data_list():
    boundary1 = OptimalBoundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
    boundary2 = OptimalBoundary(cells=[CellID('O35'), CellID('P234')])
    boundary3 = OptimalBoundary(cells=[CellID('S034'), CellID('S57')])
    data = Data('t', 'data')
    data2 = Data('t', 'data2')

    b_ds = {
        boundary1.boundary_ID.value: (boundary1, data),
        boundary2.boundary_ID.value: (boundary2, data),
        boundary3.boundary_ID.value: (boundary3, data2)
    }
    b_dataset = BoundaryDataSet(b_ds)

    assert b_dataset.get_boundary_data_list([boundary1.boundary_ID, boundary3.boundary_ID]) == [data, data2]


if __name__ == "__main__":
    test_boundary_dataset()
    test_boundary_dataset_add()
    test_boundary_dataset_get_boundary_data()
    test_boundary_dataset_get_boundary_data_list()
