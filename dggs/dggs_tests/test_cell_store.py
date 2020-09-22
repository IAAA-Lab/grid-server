import unittest
from dggs.cell_ID import CellID
from dggs.dataset.cell_dataset import CellDataSet
from dggs.store.cell_store import CellStore
from dggs.dataset.data import Data

store = CellStore()


class TestBoundaryStore(unittest.TestCase):
    def test_insert_and_all_cells(self):
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
        self.assertEqual(num_cells, len(cells))
        store.dropAll()

    def test_query_by_cell(self):
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
        self.assertEqual(num_cells, 1)
        store.dropAll()

    def test_delete_cell(self):
        store.dropAll()
        cds = CellDataSet("id")
        cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for cell in cells:
            cds.add(CellID(cell), Data(""))
        store.insert(cds)

        deleted_cells = store.delete_cell(CellID('P0'))
        self.assertEqual(deleted_cells, 1)

        stored_cells = store.query_by_cell(CellID('P0'))
        self.assertEqual(stored_cells.__len__(), 0)
        store.dropAll()

    def test_all_cell_datasets(self):
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
        self.assertEqual(num_cds, 1)
        self.assertEqual(num_cells, len(cells))
        store.dropAll()

    def test_all_cells_in_dataset(self):
        store.dropAll()
        cds = CellDataSet("id")
        cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for cell in cells:
            cds.add(CellID(cell), Data(""))
        store.insert(cds)

        stored_cds = store.query_by_cell_dataset_id("id")
        num_cds = 0
        num_cells = 0
        for cds in stored_cds:
            for cell in cds.get_cells():
                assert cells.__contains__(cell.value)
                num_cells = num_cells + 1
            num_cds = num_cds + 1
        self.assertEqual(num_cds, 1)
        self.assertEqual(num_cells, len(cells))
        store.dropAll()

    def test_query_by_cell_in_cell_datasets(self):
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
        self.assertEqual(num_cds, 1)
        self.assertEqual(num_cells, 1)
        store.dropAll()

    def test_update_cell_dataset(self):
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

        stored_cds = store.query_by_cell_dataset_id("id")
        num_cds = 0
        num_cells = 0
        for cds in stored_cds:
            for cell in cds.get_cells():
                assert cells2.__contains__(cell.value)
                num_cells = num_cells + 1
            num_cds = num_cds + 1
        self.assertEqual(num_cds, 1)
        self.assertEqual(num_cells, len(cells2))
        store.dropAll()

    def test_update_cell_in_cell_datasets(self):
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
        self.assertEqual(num_cds, 1)
        self.assertEqual(num_cells, 1)
        store.dropAll()

    def test_delete_cell_dataset(self):
        store.dropAll()
        cds = CellDataSet("id")
        cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for cell in cells:
            cds.add(CellID(cell), Data(""))
        store.insert(cds)

        deleted_cds = store.delete_cell_dataset("id")
        self.assertEqual(deleted_cds, 1)

        stored_cds = store.query_by_cell_dataset_id("id")
        self.assertEqual(stored_cds.__len__(), 0)
        store.dropAll()

    def test_delete_cell_in_cell_datasets(self):
        store.dropAll()
        cds = CellDataSet("id")
        cells = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for cell in cells:
            cds.add(CellID(cell), Data(""))
        store.insert(cds)

        deleted_cells = store.delete_cell_in_cell_datasets("id", CellID('P0'))
        self.assertEqual(deleted_cells, 1)

        stored_cds = store.query_by_cell_in_cell_datasets("id", CellID('P0'))
        num_cds = 0
        for cds in stored_cds:
            assert cds.get_cells().__len__() == 0
            num_cds = num_cds + 1
        self.assertEqual(num_cds, 1)

        store.dropAll()


if __name__ == '__main__':
    unittest.main()
