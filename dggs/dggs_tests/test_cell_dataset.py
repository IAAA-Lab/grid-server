from dggs.boundary import OptimalBoundary
from dggs.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.cell_dataset import CellDataSet
from dggs.data import Data


def test_cell_dataset():
    cell_data_set = {
        'N01': (CellID('N01'), Data('test')),
        'N02': (CellID('N02'), Data('test')),
        'N03': (CellID('N03'), Data('test'))
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    assert c_dataset.cell_data_set == cell_data_set


def test_cell_dataset_add():
    cells = [CellID('N01'), CellID('N02'), CellID('N03'), CellID('N04')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    c_dataset.add(cells[3], data)

    assert c_dataset.cells == cells


def test_cell_dataset_add_list():
    cells = [CellID('N01'), CellID('N02'), CellID('N03'), CellID('N04'), CellID('N05')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    c_dataset.add_list([(cells[3], data), (cells[4], data)])

    assert c_dataset.cells == cells


def test_get_cells():
    cells = [CellID('N01'), CellID('N02'), CellID('N03')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    assert c_dataset.get_cells() == cells


def test_get_cells_and_data():
    cells = [CellID('N01'), CellID('N02'), CellID('N03')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    cells_data = c_dataset.get_cells_and_data()

    assert cells_data == [(cells[0],data), (cells[1], data), (cells[2], data)]


def test_get_min_refinement():
    cells = [CellID('P0'), CellID('N02'), CellID('N03')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    assert c_dataset.get_min_refinement() == 1


def test_get_max_refinement():
    cells = [CellID('P0'), CellID('N02'), CellID('N033')]
    data = Data('test')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)
    assert c_dataset.get_max_refinement() == 3


def test_get_cell_data():
    cells = [CellID('P0'), CellID('N02'), CellID('N033')]
    data = Data('test')
    data2 = Data('test2')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data2)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)

    assert c_dataset.get_cell_data(CellID('N033')) == data2


def test_get_cell_data_list():
    cells = [CellID('P0'), CellID('N02'), CellID('N033')]
    data = Data('test')
    data2 = Data('test2')
    cell_data_set = {
        cells[0].value: (cells[0], data),
        cells[1].value: (cells[1], data),
        cells[2].value: (cells[2], data2)
    }

    c_dataset = CellDataSet('id', cell_data_set=cell_data_set)

    assert c_dataset.get_cell_data_list([cells[0], cells[2]]) == [data, data2]

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
    test_cell_dataset()
    test_cell_dataset_add()
    test_cell_dataset_add_list()
    test_get_cells()
    test_get_cells_and_data()
    test_get_min_refinement()
    test_get_max_refinement()
    test_get_cell_data()
    test_get_cell_data_list()
    # # test_to_JSON()
