from bson import ObjectId
from pymongo import MongoClient

import mongodb_config
from dggs.cell_ID import CellID
from dggs.cell_dataset import CellDataSet
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class CellStore:

    def __init__(self, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.dggs = dggs
        self.db = MongoClient(mongodb_config.MONGODB_CONFIG['host']).bds

    def get_Cell_Data(self, cell):
        """
        :param cell: document stored that contains the cell_id and data associated
        :return: CellID and Data tuple
        """
        return CellID(cell["cellID"]), Data(cell["data"])

    def insert(self, c_dataset):
        """
        Insert, in the collection of cell datasets, a _cellDataSet formed by its identifier.

        Insert, in the collection of cells, one _cell for each pair in the set, derived from its id,
        associated data and the identifier of the _cellDataSet.

        :param c_dataset: CellDataSet containing the CellID and Data pairs.
        """

        # Store cellDataSet
        _cellDataSet = {
            "_id": c_dataset.id,
        }
        self.db.c_data_sets.insert_one(_cellDataSet)

        # Store cells
        for (cell_id, data) in c_dataset.get_cells_and_data():
            _cell = {
                "cellID": cell_id.value,
                "data": data.content,
                "cell_dataset_id": c_dataset.id,
            }
            self.db.cells.insert_one(_cell)

    """
    CELLS
    """

    def all_cells(self):
        """
        :return: List of all stored Cells and Data associated
        """
        cells_founded = self.db.cells.find()
        cells = []
        for cell in cells_founded:
            cell, data = self.get_Cell_Data(cell)
            cells.append((cell, data))
        return cells

    def query_by_cell(self, cell_id):
        """
        :param cell_id: CellID
        :return: List of tuples with stored cells that have the same identifier as the param and data associated
        """
        cells_founded = self.db.cells.find({"cellID": cell_id.value})
        cells = []
        for cell in cells_founded:
            cell, data = self.get_Cell_Data(cell)
            cells.append((cell, data))
        return cells

    def query_by_polygon(self, polygon):
        return []

    def delete_cell(self, cell_id):
        """
        :param cell_id: CellID
        :return: Delete stored cells that have the same identifier as the param
        """
        result = self.db.cells.delete_many({"cellID": cell_id.value})

        return result.deleted_count

    """
    CELLS_DATASETS
    """

    def all_cell_datasets(self):
        """
        :return: List of all stored CellDatasets
        """
        cell_data_sets = []
        cell_datasets_founded = self.db.c_data_sets.find()
        for cell_dataset in cell_datasets_founded:
            cds = CellDataSet(id=cell_dataset["_id"])
            cells_in_cds_founded = self.db.cells.find({"cell_dataset_id": cell_dataset["_id"]})
            for cell in cells_in_cds_founded:
                cds.add(CellID(cell['cellID']), Data(cell["data"]))
            cell_data_sets.append(cds)
        return cell_data_sets

    def query_by_cell_to_cell_datasets(self, cell_id):
        """
        :param cell_id: CellID
        :return: List of CellDataSets where cell_id is located
        """
        cells_founded = self.db.cells.find({"id": cell_id.value})

        cell_data_sets = []
        for cell in cells_founded:
            cds = CellDataSet()
            cells_in_bds_founded = self.db.cells.find(
                {"cell_dataset_id": cell["cell_dataset_id"]})
            for cell_2 in cells_in_bds_founded:
                cell, data = self.get_Cell_Data(cell_2)
                cds.add(cell, data)
            cell_data_sets.append(cds)
        return cell_data_sets

    def all_cells_in_dataset(self, id):
        """
        :param id: identifier of the CellDataset
        :return: List of tuples with stored cells and data associated stored in the CellDataset with that id.
        """
        cell_datasets_founded = self.db.c_data_sets.find({"_id": id})
        cell_data_sets = []
        for cell_dataset in cell_datasets_founded:
            cds = CellDataSet(id=id)
            cells_in_cds_founded = self.db.cells.find({"cell_dataset_id": cell_dataset["_id"]})
            for cell in cells_in_cds_founded:
                cds.add(CellID(cell['cellID']), Data(cell["data"]))
            cell_data_sets.append(cds)
        return cell_data_sets

    def query_by_cell_in_cell_datasets(self, id, cell_id):
        """
        :param id: identifier of the CellDataset
        :param cell_id: CellID
        :return: Cell and data associated stored in the CellDataset with that id.
        """
        cell_datasets_founded = self.db.c_data_sets.find({"_id": id})
        cell_data_sets = []
        for cell_dataset in cell_datasets_founded:
            cds = CellDataSet(id=id)
            cells_in_cds_founded = self.db.cells.find({"cell_dataset_id": cell_dataset["_id"],
                                                                "cellID":cell_id.value})
            for cell in cells_in_cds_founded:
                cds.add(CellID(cell['cellID']), Data(cell["data"]))
            cell_data_sets.append(cds)
        return cell_data_sets

    def update_cell_dataset(self, cds):
        """
        :param cds:
        :return: Update the CellDataset with that id.
        """
        cell_datasets_founded = self.db.c_data_sets.find({"_id": cds.id})
        for cell_dataset in cell_datasets_founded:
            self.db.cells.delete_many({"cell_dataset_id": cds.id})
            for (cell, data) in cds.get_cells_and_data():
                _cell = {
                    "cellID": cell.value,
                    "data": data.content,
                    "cell_dataset_id": cell_dataset["_id"]
                }
                self.db.cells.insert_one(_cell)

    def update_cell_in_cell_datasets(self, cds_id, cell_id, data):
        """
        :param cds_id: identifier of the CellDataset
        :param cell_id: CellID
        :return: Update the stored cell that have the same identifier as the param in the CellDataset with that id.
        """
        cell_datasets_founded = self.db.c_data_sets.find({"_id": cds_id})
        for cell_dataset in cell_datasets_founded:
            myquery = {"cellID": cell_id.value, "cell_dataset_id": cell_dataset["_id"],}
            newvalues = {"$set": {"data": data.content}}

            return self.db.cells.update_many(myquery, newvalues)

    def delete_cell_dataset(self, id):
        """
        :param id: identifier of the CellDataset
        :return: Delete the CellDataset with that id and all the cells and data in it.
        """
        result1 = self.db.c_data_sets.delete_many({"_id": id})

        if result1.deleted_count > 0:
            self.db.cells.delete_many({"cell_dataset_id": id})

        return result1.deleted_count

    def delete_cell_in_cell_datasets(self, id, cell_id):
        """
        :param id: identifier of the BoundaryDataset
        :param cell_id: CellID
        :return: Delete the stored cell that have the same identifier as the param in the CellDataset with that id.
        """

        result = self.db.cells.delete_many({"cell_dataset_id": id,
                                                                "cellID": cell_id.value})

        return result.deleted_count


    def dropAll(self):
        """
        Delete stored data
        """
        self.db.cells.drop()
        self.db.c_data_sets.drop()