import json

from dggs.boundary_ID import BoundaryID
from dggs.cell_ID import CellID
from dggs.dataset.data import Data
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
        return self.cells

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

    def get_geodetic_coordinates(self):
        """
        :return: list of geodetic coordinates of the vertices of each cell of the celldataset
        (upper left, upper right, lower left, lower right, nucleus)
        """
        gC = []
        for cell in self.cells:
            gC.append(self.dggs.get_cell_geodetic_coordinates(cell))
        return gC

    def get_limit_cells(self):
        """
        :return: Top cell, bottom cell, leftmost cell, and rightmost cell
        """
        top_cell = self.cells[0]
        bottom_cell = self.cells[0]
        for cell in self.cells:
            if self.dggs.up(cell, top_cell):
                top_cell = cell
            if self.dggs.down(cell, bottom_cell):
                bottom_cell = cell

        left_cell = self.cells[0]
        right_cell = self.cells[0]
        for cell in self.cells:
            if self.dggs.left(cell, left_cell):
                left_cell = cell
            if self.dggs.right(cell, right_cell):
                right_cell = cell

        return top_cell, bottom_cell, left_cell, right_cell

    def get_bbox(self, projected=False):
        """
        :return: geodetic coordinates of the bbox of the cell dataset
        [lower left, lower right, upper right, upper left, lower left]

        """
        if len(self.cells) == 1:
            ul = self.dggs.get_cell_projected_coordinates(self.cells[0])[0]
            dr = self.dggs.get_cell_projected_coordinates(self.cells[0])[3]
            bounds = [ul, dr]
            bbox_bounds = self.dggs.get_geodetic_coordinates_from_bbox(
                [[bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[0][1]],
                 [bounds[0][0], bounds[1][1]], [bounds[1][0], bounds[1][1]]])
        else:
            top_cell, below_cell, left_cell, right_cell = self.get_limit_cells()

            if top_cell == left_cell:
                ul = self.dggs.get_cell_projected_coordinates(top_cell)[0]
            else:
                ul = (self.dggs.get_cell_projected_coordinates(left_cell)[0][0],
                      self.dggs.get_cell_projected_coordinates(top_cell)[0][1])

            if below_cell == right_cell:
                dr = self.dggs.get_cell_projected_coordinates(below_cell)[3]
            else:
                dr = (self.dggs.get_cell_projected_coordinates(right_cell)[3][0],
                      self.dggs.get_cell_projected_coordinates(below_cell)[3][1])

            bounds = [ul, dr]
            bbox_bounds = [[bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[0][1]],
                           [bounds[0][0], bounds[1][1]], [bounds[1][0], bounds[1][1]]]
            if not projected:
                if self.dggs.check_bounds(bbox_bounds):
                    bbox_bounds = self.dggs.get_geodetic_coordinates_from_bbox(bbox_bounds)
                else:
                    up = -90
                    left = 180
                    down = 90
                    right = -180
                    for cell in [top_cell, left_cell, below_cell, right_cell]:
                        cell_coords = self.dggs.get_cell_geodetic_coordinates(cell)
                        for coord in cell_coords:
                            if coord[1] > up:
                                up = coord[1]
                            if coord[0] < left:
                                left = coord[0]
                            if coord[1] < down:
                                down = coord[1]
                            if coord[0] > right:
                                right = coord[0]

                    ul = (left, up)
                    dr = (right, down)
                    bounds = [ul, dr]
                    bbox_bounds = [[bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[0][1]],
                                   [bounds[0][0], bounds[1][1]], [bounds[1][0], bounds[1][1]]]

        return [[bbox_bounds[2], bbox_bounds[3],
                 bbox_bounds[1], bbox_bounds[0],
                 bbox_bounds[2]]]

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
        return json.dumps(cds)

    def fromJSON(self, cds, file=False):
        if file:
            cds = json.load(cds)
        self.cell_data_set = {}
        self.id = cds['id']
        cell_list = cds['cell_data_set']

        for cell in cell_list:
            self.add(CellID(cell['cellID']), Data(cell['data']))

        return self