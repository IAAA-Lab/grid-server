import json

from dggs import cell_ID
from dggs.boundary_ID import BoundaryID
from dggs.cell_ID import CellID
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class CellDataSet:

    def __init__(self, id, dggs=rHEALPix(N_side=3, north_square=0, south_square=0), cell_data_set=None):
        """
        :param boundary_ID: boundary identifier, of type BoundaryID
        :param cells: list of identifiers of the cells that make up the boundary, [ CellID, CellID ... ]
        :param dggs: Discrete Global Grid System, rHEALPix by default
        :param cell_data_set: dictionary with CellID.value as key and  (CellID, Data) as value:
        {
            CellID.value: (CellID, Data)
        }
        """
        assert id is not None
        self.id = id

        self.boundary_ID = ''
        self.cells = []
        self.optimal = False
        self.tree = []
        self.grid_stack = []
        self.dggs = dggs

        if cell_data_set is None:
            cell_data_set = {}
        else:
            cells = []
            for id, (cell_id, data) in cell_data_set.items():
                if cell_id not in self.cells:
                    cells.append(cell_id)
                else:
                    print('Cell already exists in this dataset')
            cell_ids = sorted([cell.value for cell in cells])
            self.cells = [CellID(id) for id in cell_ids]

            boundary_ID = ''
            for cell_ID in self.cells:
                boundary_ID = boundary_ID + cell_ID.value
            self.boundary_ID = BoundaryID(boundary_ID)
        self.cell_data_set = cell_data_set


    def add(self, cell_id, data):
        """
        Add a pair (CellID, Data)
        :param cell_id: object of type CellID.
        :param data: object of type Data.
        """
        if cell_id not in self.cells:
            self.cells.append(cell_id)
            cell_ids = sorted([cell.value for cell in self.cells])
            self.cells = [CellID(id) for id in cell_ids]

            boundary_ID = ''
            for cell_ID in self.cells:
                boundary_ID = boundary_ID + cell_ID.value
            self.boundary_ID = BoundaryID(boundary_ID)

            self.cell_data_set[cell_id.value] = (cell_id, data)
        else:
            print('Cell already exists in this dataset')
            return -1

    def add_list(self, cell_data_list):
        """
        Add all pairs (CellID, Data) in a list
        :paramcell_data_list: list of cells and associated data tuples
        """
        for (cell_id, data) in cell_data_list:
            if cell_id not in self.cells:
                self.cells.append(cell_id)
                self.cell_data_set[cell_id.value] = (cell_id, data)
            else:
                print('Cell already exists in this dataset')
                return -1

        cell_ids = sorted([cell.value for cell in self.cells])
        self.cells = [CellID(id) for id in cell_ids]

        boundary_ID = ''
        for cell_ID in self.cells:
            boundary_ID = boundary_ID + cell_ID.value
        self.boundary_ID = BoundaryID(boundary_ID)

    def get_cells(self):
        """
        :return: list with all the cells of the set
        """
        cell_list = []
        for id, (cell_id, data) in self.cell_data_set.items():
            cell_list.append(cell_id)
        return cell_list

    def get_cells_and_data(self):
        """
        :return: list of tuples (CellID, Data) with all the cells and data of the set
        """
        cell_data_list = []
        for id, (cell_id, data) in self.cell_data_set.items():
            cell_data_list.append((cell_id, data))
        return cell_data_list

    def get_min_refinement(self):
        """
        :return: integer that represents the minimum refinement of the set
        """
        cell_id, data = list(self.cell_data_set.values())[0]
        min_refinement = cell_id.get_refinement()
        for id, (cell_id, data) in self.cell_data_set.items():
            if cell_id.get_refinement() < min_refinement:
                min_refinement = cell_id.get_refinement()
        return min_refinement

    def get_max_refinement(self):
        """
        :return: integer that represents the maximum refinement of the set
        """
        cell_id, data = list(self.cell_data_set.values())[0]
        max_refinement = cell_id.get_refinement()
        for id, (cell_id, data) in self.cell_data_set.items():
            if cell_id.get_refinement() > max_refinement:
                max_refinement = cell_id.get_refinement()
        return max_refinement

    def get_cell_data(self, cell_id):
        """
        :param cell_id: cell identifier, of type CellID
        :return: data associated with the cell with identifier cell_id
        """
        return self.cell_data_set[cell_id.value][1]

    def get_cell_data_list(self, cell_id_list):
        """
        :param cell_id_list: list of cell identifiers, of type CellID
        :return: list of data associated with the cells with identifier cell_id
        """
        data_list = []
        for cell_id in cell_id_list:
            data_list.append(self.cell_data_set[cell_id.value][1])
        return data_list

    def print(self):
        """
        Prints the pairs of cell identifiers with their associated data from the set.
        """
        for id, (cell_id, data) in self.cell_data_set.items():
            print(cell_id.value, data.content)

    def toJSON(self):
        cell_list = []
        for id, (cell_id, data) in self.cell_data_set.items():
            dic = {
                'cellID': id,
                'data': data.content
            }
            cell_list.append(dic)

        cds = {
            'id': self.id,
            'cell_data_set': cell_list,
        }
        print(cds)
        return json.dumps(cds)

    def fromJSON(self, cds_json):
        cds = json.loads(cds_json)
        self.cell_data_set = {}
        self.id = cds['id']
        cell_list = cds['cell_data_set']

        for cell in cell_list:
            self.add(CellID(cell['cellID']), Data(cell['data']))

        return self
