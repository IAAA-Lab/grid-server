from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.cell_dataset import CellDataSet
from dggs.cell_store import CellStore
from dggs.data import Data

store = CellStore()


def test_insert_and_all_cells():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    stored_cells = store.all_cells()
    num_cells = 0
    for cell in stored_cells:
        assert cells.__contains__(cell[0].value)
        num_cells = num_cells + 1
    assert num_cells == len(cells)
    store.dropAll()


def test_query_by_cell():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    stored_cells = store.query_by_cell(CellID('P0'))
    num_cells = 0
    for cell in stored_cells:
        assert cells.__contains__(cell[0].value)
        num_cells = num_cells + 1
    assert num_cells == 1
    store.dropAll()


def test_delete_cell():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    deleted_cells = store.delete_cell(CellID('P0'))
    assert deleted_cells == 1

    stored_cells = store.query_by_cell(CellID('P0'))
    assert stored_cells.__len__() == 0
    store.dropAll()


def test_all_cell_datasets():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    stored_cds = store.all_cell_datasets()
    num_cds = 0
    num_cells = 0
    for cds in stored_cds:
        for cell in cds.get_cells():
            assert cells.__contains__(cell.value)
            num_cells = num_cells + 1
        num_cds = num_cds + 1
    assert num_cds == 1
    assert num_cells == len(cells)
    store.dropAll()


def test_all_cells_in_dataset():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    stored_cds = store.all_cells_in_dataset("id")
    num_cds = 0
    num_cells = 0
    for cds in stored_cds:
        for cell in cds.get_cells():
            assert cells.__contains__(cell.value)
            num_cells = num_cells + 1
        num_cds = num_cds + 1
    assert num_cds == 1
    assert num_cells == len(cells)
    store.dropAll()


def test_query_by_cell_in_cell_datasets():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    stored_cds = store.query_by_cell_in_cell_datasets("id", CellID('P0'))
    num_cds = 0
    num_cells = 0
    for cds in stored_cds:
        for cell in cds.get_cells():
            assert cells.__contains__(cell.value)
            num_cells = num_cells + 1
        num_cds = num_cds + 1
    assert num_cds == 1
    assert num_cells == 1
    store.dropAll()


def test_update_cell_dataset():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    cds2 = CellDataSet("id")
    cells2 = ['O0', 'O1', 'O2', 'O3', 'O4']

    for cell in cells2:
        cds2.add(CellID(cell), Data(""))
    store.update_cell_dataset(cds2)

    stored_cds = store.all_cells_in_dataset("id")
    num_cds = 0
    num_cells = 0
    for cds in stored_cds:
        for cell in cds.get_cells():
            assert cells2.__contains__(cell.value)
            num_cells = num_cells + 1
        num_cds = num_cds + 1
    assert num_cds == 1
    assert num_cells == len(cells2)
    store.dropAll()


def test_update_cell_in_cell_datasets():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    store.update_cell_in_cell_datasets("id", CellID('P0'), Data("test"))

    stored_cds = store.query_by_cell_in_cell_datasets("id", CellID('P0'))
    num_cds = 0
    num_cells = 0
    for cds in stored_cds:
        for cell, data in cds.get_cells_and_data():
            assert cells.__contains__(cell.value)
            assert data.content == Data("test").content
            num_cells = num_cells + 1
        num_cds = num_cds + 1
    assert num_cds == 1
    assert num_cells == 1
    store.dropAll()


def test_delete_cell_dataset():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    deleted_cds = store.delete_cell_dataset("id")
    assert deleted_cds == 1

    stored_cds = store.all_cells_in_dataset("id")
    assert stored_cds.__len__() == 0
    store.dropAll()


def test_delete_cell_in_cell_datasets():
    store.dropAll()
    cds = CellDataSet("id")
    cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

    for cell in cells:
        cds.add(CellID(cell), Data(""))
    store.insert(cds)

    deleted_cells = store.delete_cell_in_cell_datasets("id", CellID('P0'))
    assert deleted_cells == 1

    stored_cds = store.query_by_cell_in_cell_datasets("id",  CellID('P0'))
    num_cds = 0
    for cds in stored_cds:
        assert cds.get_cells().__len__() == 0
        num_cds = num_cds + 1
    assert num_cds == 1

    store.dropAll()


def test_query_by_polygon():
    # TODO
    pass


if __name__ == "__main__":
    test_insert_and_all_cells()
    test_delete_cell()
    test_all_cell_datasets()
    test_all_cells_in_dataset()
    test_query_by_cell_in_cell_datasets()
    test_update_cell_dataset()
    test_update_cell_in_cell_datasets()
    test_delete_cell_dataset()
    test_delete_cell_in_cell_datasets()
    #test_query_by_polygon()
