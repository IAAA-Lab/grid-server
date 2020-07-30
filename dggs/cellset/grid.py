import networkx as nx

from dggs.boundary_ID import BoundaryID
from dggs.cell_ID import CellID
from dggs.rHealPix import rHEALPix


class Grid:
    def __init__(self, refinement_level, boundary_ID=None, cells=None,
                 dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param refinement_level
        :param boundary_ID: boundary identifier, of type BoundaryID
        :param cells: list of identifiers of the cells that make up the boundary, [ CellID, CellID ... ]
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.boundary_ID = boundary_ID
        self.cells = cells
        self.dggs = dggs
        self.refinement_level = refinement_level

        assert boundary_ID is not None or cells is not None

        if cells is None:
            cells = []
            cell_ID = ''
            first = True
            for char in boundary_ID.value:
                if char in self.dggs.cells_R0:
                    if not first:
                        cells.append(CellID(cell_ID))
                    else:
                        first = False
                    cell_ID = char
                else:
                    cell_ID = cell_ID + char
            cells.append(CellID(cell_ID))
            cell_ids = sorted([cell.value for cell in cells])
            self.cells = [CellID(id) for id in cell_ids]

        if boundary_ID is None:
            cell_ids = sorted([cell.value for cell in cells])
            self.cells = [CellID(id) for id in cell_ids]
            boundary_ID = ''
            for cell_ID in self.cells:
                boundary_ID = boundary_ID + cell_ID.value
            self.boundary_ID = BoundaryID(boundary_ID)

    def get_refinement_level(self):
        return self.refinement_level

    def get_as_tree(self):
        """
        :return: prefix tree / trie composed of the identifiers of the boundary cells
        """
        cell_ids = [cell.value for cell in self.cells]
        sorted_cell_ids = sorted(cell_ids)
        t, r = nx.prefix_tree(sorted_cell_ids)  # A Prefix_Tree is essentially another name for a trie
        return t

    def get_as_grid_stack(self):
        """
        :return:
        """

    def get_min_refinement(self):
        """
        :return: integer that represents minimum refinement
        """
        return self.refinement_level

    def get_max_refinement(self):
        """
        :return: integer that represents maximum refinement
        """
        return self.refinement_level
