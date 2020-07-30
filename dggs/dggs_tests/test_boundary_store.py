from dggs.cellset.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.dataset.boundary_dataset import BoundaryDataSet
from dggs.store.boundary_store import BoundaryStore
from dggs.dataset.data import Data

store = BoundaryStore()


def test_insert_and_all_boudnaries():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    stored_boundaries = store.all_boundaries()
    num_boundaries = 0
    for boundary in stored_boundaries:
        assert boundaries.__contains__(boundary[0].AUID_to_CUIDs())
        num_boundaries = num_boundaries + 1
    assert num_boundaries == len(boundaries)
    store.dropAll()


def test_query_by_boundary():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    stored_boundaries = store.query_by_boundary((Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    num_boundaries = 0
    for boundary in stored_boundaries:
        assert boundaries.__contains__(boundary[0].AUID_to_CUIDs())
        num_boundaries = num_boundaries + 1
    assert num_boundaries == 1
    store.dropAll()


def test_delete_boundary():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    deleted_boundaries = store.delete_boundary((Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    assert deleted_boundaries == 1

    stored_boundaries = store.query_by_boundary((Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    assert stored_boundaries.__len__() == 0
    store.dropAll()


def test_all_boundary_dataset():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    stored_bds = store.all_boundary_datasets()
    num_bds = 0
    num_boundaries = 0
    for bds in stored_bds:
        for boundary in bds.get_boundaries():
            assert boundaries.__contains__(boundary.AUID_to_CUIDs())
            num_boundaries = num_boundaries + 1
        num_bds = num_bds + 1
    assert num_bds == 1
    assert num_boundaries == len(boundaries)
    store.dropAll()


def test_all_boundaries_in_dataset():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    stored_bds = store.query_by_boundary_dataset_id("id")
    num_bds = 0
    num_boundaries = 0
    for bds in stored_bds:
        for boundary in bds.get_boundaries():
            assert boundaries.__contains__(boundary.AUID_to_CUIDs())
            num_boundaries = num_boundaries + 1
        num_bds = num_bds + 1
    assert num_bds == 1
    assert num_boundaries == len(boundaries)
    store.dropAll()


def test_query_by_boundary_in_boundary_datasets():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    stored_bds = store.query_by_boundary_in_boundary_datasets("id", (Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    num_bds = 0
    num_boundaries = 0
    for bds in stored_bds:
        for boundary in bds.get_boundaries():
            assert boundaries.__contains__(boundary.AUID_to_CUIDs())
            num_boundaries = num_boundaries + 1
        num_bds = num_bds + 1
    assert num_bds == 1
    assert num_boundaries == 1
    store.dropAll()

def test_update_boundary_dataset():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    bds2 = BoundaryDataSet("id")
    boundaries2 = ['N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries2:
        bds2.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.update_boundary_dataset(bds2)

    stored_bds = store.query_by_boundary_dataset_id("id")
    num_bds = 0
    num_boundaries = 0
    for bds in stored_bds:
        for boundary in bds.get_boundaries():
            assert boundaries2.__contains__(boundary.AUID_to_CUIDs())
            num_boundaries = num_boundaries + 1
        num_bds = num_bds + 1
    assert num_bds == 1
    assert num_boundaries == len(boundaries2)
    store.dropAll()


def test_update_cell_in_cell_datasets():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    store.update_boundary_in_boundary_datasets("id", (Boundary(boundary_ID=BoundaryID('O23P12P34S56'))), Data("test"))

    stored_bds = store.query_by_boundary_in_boundary_datasets("id", (Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    num_bds = 0
    num_boundaries = 0
    for bds in stored_bds:
        for boundary, data in bds.get_boundaries_and_data():
            assert boundaries.__contains__(boundary.AUID_to_CUIDs())
            assert data.content == Data("test").content
            num_boundaries = num_boundaries + 1
        num_bds = num_bds + 1
    assert num_bds == 1
    assert num_boundaries == 1
    store.dropAll()


def test_delete_boundary_dataset():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    deleted_bds = store.delete_boundary_dataset("id")
    assert deleted_bds == 1

    stored_bds = store.query_by_boundary_dataset_id("id")
    assert stored_bds.__len__() == 0
    store.dropAll()


def test_delete_boundary_in_boundary_datasets():
    store.dropAll()
    bds = BoundaryDataSet("id")
    boundaries = ['O23P12P34S56', 'P10P11P2', 'N0', 'N8O2P0', 'O6S0S1S2', 'Q']

    for boundary in boundaries:
        bds.add(Boundary(boundary_ID=BoundaryID(boundary)), Data(""))
    store.insert(bds)

    deleted_boundaries = store.delete_boundary_in_boundary_datasets("id",
                                                                    (Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    assert deleted_boundaries == 1

    stored_bds = store.query_by_boundary_in_boundary_datasets("id", (Boundary(boundary_ID=BoundaryID('O23P12P34S56'))))
    num_bds = 0
    for bds in stored_bds:
        assert bds.get_boundaries().__len__() == 0
        num_bds = num_bds + 1
    assert num_bds == 1

    store.dropAll()


def test_query_by_polygon():
    # TODO
    pass


if __name__ == "__main__":
    test_insert_and_all_boudnaries()
    test_delete_boundary()
    test_all_boundary_dataset()
    test_all_boundaries_in_dataset()
    test_query_by_boundary_in_boundary_datasets()
    test_update_boundary_dataset()
    test_update_cell_in_cell_datasets()
    test_delete_boundary_dataset()
    test_delete_boundary_in_boundary_datasets()
    #test_query_by_polygon()
