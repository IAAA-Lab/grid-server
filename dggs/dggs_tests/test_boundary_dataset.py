from dggs.boundary import OptimalBoundary
from dggs.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.data import Data


def test_boundary_dataset():
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
    assert b_dataset.boundary_data_set == b_ds


def test_boundary_dataset_add():
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
    assert b_dataset.boundary_data_set == b_ds2


def test_boundary_dataset_add_list():
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
    assert b_dataset.boundary_data_set == b_ds2


def test_get_boundaries():
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

    assert boundaries == [boundary1, boundary2, boundary3]


def test_get_boundaries_and_data():
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

    assert boundaries_data == [(boundary1, data), (boundary2, data), (boundary3, data)]


def test_get_min_refinement():
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

    assert b_dataset.get_min_refinement() == 0


def test_get_max_refinement():
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

    assert b_dataset.get_max_refinement() == 5


def test_get_boundary_data():
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

    assert b_dataset.get_boundary_data(boundary3.boundary_ID) == data2


def test_get_boundary_data_list():
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

    assert b_dataset.get_boundary_data_list([boundary1.boundary_ID, boundary3.boundary_ID]) == [data, data2]

def test_to_JSON():
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
    print(b_dataset.toJSON())

    b_dataset_2 = BoundaryDataSet('').fromJSON(b_dataset.toJSON())
    b_dataset_2.print()



if __name__ == "__main__":
    test_boundary_dataset()
    test_boundary_dataset_add()
    test_boundary_dataset_add_list()
    test_get_boundaries()
    test_get_boundaries_and_data()
    test_get_min_refinement()
    test_get_max_refinement()
    test_get_boundary_data()
    test_get_boundary_data_list()
    # test_to_JSON()
