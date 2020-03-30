from dggs.dggs_auids.dggs_auids import cuids_to_bp_auid, bp_auid_to_cuids
from dggs.boundary_ID import BoundaryID, AUID
from dggs.cell_ID import CellID
from dggs.rHealPix import rHEALPix
import networkx as nx


class Boundary:
    def __init__(self, boundary_ID=None, cells=None, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param boundary_ID: boundary identifier, of type BoundaryID
        :param cells: list of identifiers of the cells that make up the boundary, [ CellID, CellID ... ]
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.boundary_ID = boundary_ID
        self.cells = cells
        self.optimal = False
        self.tree = []
        self.grid_stack = []
        self.dggs = dggs

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
            self.cells = cells

        if boundary_ID is None:
            boundary_ID = ''
            for cell_ID in cells:
                boundary_ID = boundary_ID + cell_ID.value
            self.boundary_ID = BoundaryID(boundary_ID)

    def get_as_tree(self):
        """
        :return: prefix tree / trie composed of the identifiers of the boundary cells
        """
        cell_ids = [cell.value for cell in self.cells]
        sorted_cell_ids = sorted(cell_ids)
        t, r = nx.prefix_tree(sorted_cell_ids)  # A Prefix_Tree is essentially another name for a trie
        return t

    def get_as_grid_stack(self):
        # TODO
        return self.grid_stack

    def get_min_refinement(self):
        """
        :return: integer that represents minimum refinement of the boundary, that is,
        of the cells that compose it, the refinement of the cell with the lowest refinement.
        """
        min_refinement = self.cells[0].get_refinement()
        for cell in self.cells:
            if cell.get_refinement() < min_refinement:
                min_refinement = cell.get_refinement()
        return min_refinement

    def get_max_refinement(self):
        """
        :return: integer that represents maximum refinement of the boundary, that is,
        of the cells that compose it, the refinement of the cell with the highest refinement.
        """
        max_refinement = self.cells[0].get_refinement()
        for cell in self.cells:
            if cell.get_refinement() > max_refinement:
                max_refinement = cell.get_refinement()
        return max_refinement

    def print_cells(self):
        """
        Prints the value of the identifier of each cell of the boundary
        """
        for cell_id in self.cells:
            print(cell_id.value)

    def is_optimal(self):
        """
        :return: True if the boundary is optimal or False if it is not.
        """
        return self.optimal

    def optimize(self):
        """
        :return: OptimalBoundary, that is, a boundary that is the smallest one that delimits exactly its area.
        """
        maxrefinement = self.get_max_refinement()
        new_cells = self.cells
        for actual_refinement in range(maxrefinement, 0, -1):
            for cell_act_res in [cell for cell in new_cells if cell.get_refinement() == actual_refinement]:
                father_value = cell_act_res.value[actual_refinement - 1]
                cells_with_same_father = [cell for cell in new_cells
                                          if (cell.get_refinement() == actual_refinement
                                              and cell.value[actual_refinement - 1] == father_value)]
                if len(cells_with_same_father) == (self.dggs.N_side ** 2):
                    new_cells = [cell for cell in new_cells if cell not in cells_with_same_father]
                    copy_cell_value = cell_act_res.value
                    new_cells.append(CellID(copy_cell_value[:actual_refinement]))

        cell_ids = sorted([cell.value for cell in new_cells])
        new_cells = [CellID(ciud) for ciud in cell_ids]
        auid_bp, _, _, _, _ = cuids_to_bp_auid(cell_ids, pars="()", with_opening_par=False)
        return OptimalBoundary(boundary_ID=AUID(auid_bp), cells=new_cells)

    def get_projected_coordinates(self):
        """
        :return: list of projected coordinates of the vertices of each cell of the boundary
        (upper left, upper right, lower left, lower right, nucleus)
        """
        pC = []
        for cell in self.cells:
            pC.append(self.dggs.get_cell_projected_coordinates(cell))
        return pC

    def get_geodetic_coordinates(self):
        """
        :return: list of geodetic coordinates of the vertices of each cell of the boundary
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

    def get_bbox(self):
        """
        :return: geodetic coordinates of the boundary's bbox
        [lower left, lower right, upper right, upper left, lower left]

        If the boundary is formed by a single cell, it calculates the upper left
        and lower right vertex of it.

        If the boundary is made up of more than one cell, it calculates the upper left
        and lower right vertex of the bbox from the upper left and lower right cells
        respectively.
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
                ul = self.dggs.get_cell_projected_coordinates(top_cell)[0]  # TODO ¿Mejor vértice o centro?
            else:
                ul = (self.dggs.get_cell_projected_coordinates(left_cell)[0][0],
                      self.dggs.get_cell_projected_coordinates(top_cell)[0][1])

            if below_cell == right_cell:
                dr = self.dggs.get_cell_projected_coordinates(below_cell)[3]  # TODO ¿Mejor vértice o centro?
            else:
                dr = (self.dggs.get_cell_projected_coordinates(right_cell)[3][0],
                      self.dggs.get_cell_projected_coordinates(below_cell)[3][1])

            bounds = [ul, dr]
            bbox_bounds = [[bounds[0][0], bounds[0][1]], [bounds[1][0], bounds[0][1]],
                           [bounds[0][0], bounds[1][1]], [bounds[1][0], bounds[1][1]]]
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


class OptimalBoundary(Boundary):
    def __init__(self, boundary_ID=None, cells=None, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param boundary_ID: boundary identifier, as defined in the AGILE19 paper, of type AUID
        :param cells: list of identifiers of the cells that make up the boundary, [ CellID, CellID ... ]
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.boundary_ID = boundary_ID
        self.cells = cells
        self.optimal = True
        self.tree = []
        self.grid_stack = []
        self.dggs = dggs

        assert boundary_ID is not None or cells is not None

        if cells is None:
            cells = bp_auid_to_cuids(boundary_ID.value, pars="()", with_opening_par=False)
            self.cells = []
            for cell in cells:
                self.cells.append(CellID(cell))
        if boundary_ID is None:
            cuids = [cell.value for cell in self.cells]
            auid_bp, _, _, _, _ = cuids_to_bp_auid(cuids, pars="()", with_opening_par=False)
            self.boundary_ID = AUID(auid_bp)

    def optimize(self):
        """
        :return: OptimalBoundary, that is, a boundary that is the smallest one that delimits exactly its area.
        """
        return self