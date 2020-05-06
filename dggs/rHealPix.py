import decimal
import math
from itertools import product

from numpy import pi, base_repr
from pyproj import Proj
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from dggs.cell_ID import CellID


class rHEALPix():
    # Refinement 0 cell identifiers (different from other levels)
    cells_R0 = ['N', 'O', 'P', 'Q', 'R', 'S']
    # Row-column coordinates of Refinement 0 cells
    coords_R0 = {
        'N': (0, 0),
        'O': (1, 0),
        'P': (1, 1),
        'Q': (1, 2),
        'R': (1, 3),
        'S': (2, 0),
    }
    R_q = 6374581.4671
    Ratio = 0.998882147091

    def __init__(self, N_side=3, north_square=0, south_square=0, max_area=1):
        """
        :param N_side: integer, minimum 2, so that each cell has N_side x N_side child cells.
        :param north_square: integer between 0 and 3 that indicate the position of the north polar square
        :param south_square: integer between 0 and 3 that indicate the position of the south polar square
        :param max_area: area, in square meters, of the smallest ellipsoidal grid cells
        """
        self.N_side = N_side

        assert north_square < 4
        assert south_square < 4
        self.north_square = north_square
        self.south_square = south_square

        # For the area of an ellipsoidal cell to be at most A square meters,
        # the refinement must be at least ⌈log (Rq2 (2π/3) A−1) / (2 log (Nside))⌉
        self.max_area = max_area
        self.max_refinement = int(math.ceil(
            math.log(rHEALPix.Ratio ** 2 * (2 * pi / 3) * self.max_area ** -1) / (2 * math.log(N_side))))

        # Row-column coordinates of cells with a refinement greater than 0.
        rowcol_cells = {}
        for (row, col) in product(list(range(N_side)), repeat=2):
            order = row * N_side + col
            rowcol_cells[(row, col)] = order
            rowcol_cells[order] = (row, col)
        self.rowcol_cells = rowcol_cells

        # Coordinates of the upper left vertices of the refinement cells 0
        self.R0_ul_vertex = {
            self.cells_R0[0]: ((-pi + self.north_square * pi / 2) * self.Ratio, (3 * pi / 4) * self.Ratio),
            self.cells_R0[1]: (-pi * self.Ratio , (pi / 4) * self.Ratio),
            self.cells_R0[2]: ((-pi / 2) * self.Ratio, (pi / 4) * self.Ratio),
            self.cells_R0[3]: (0 * self.Ratio , (pi / 4) * self.Ratio),
            self.cells_R0[4]: ((pi / 2) * self.Ratio, (pi / 4) * self.Ratio),
            self.cells_R0[5]: ((-pi + self.south_square * pi / 2) * self.Ratio, (-pi / 4)* self.Ratio)
        }

        # Unfolded cube polygon
        self.polygon = Polygon([(-pi * rHEALPix.Ratio, -3 / 4 * pi * rHEALPix.Ratio),
                           (-1 / 2 * pi * rHEALPix.Ratio, -3 / 4 * pi * rHEALPix.Ratio),
                           (-1 / 2 * pi * rHEALPix.Ratio, -1 / 4 * pi * rHEALPix.Ratio),
                           (pi * rHEALPix.Ratio, -1 / 4 * pi * rHEALPix.Ratio),
                           (pi * rHEALPix.Ratio, 1 / 4 * pi * rHEALPix.Ratio),
                           (-1 / 2 * pi * rHEALPix.Ratio, 1 / 4 * pi * rHEALPix.Ratio),
                           (-1 / 2 * pi * rHEALPix.Ratio, 3 / 4 * pi * rHEALPix.Ratio),
                           (-pi * rHEALPix.Ratio, 3 / 4 * pi * rHEALPix.Ratio),
                           (-pi * rHEALPix.Ratio, -3 / 4 * pi * rHEALPix.Ratio)])

        self.proj = Proj(proj='rhealpix', a=1, ellps='WGS84', south_square=self.south_square,
                         north_square=self.north_square, lon_0=0, preserve_units=False)

    def cell_width(self, refinement):
        """
        :param refinement: the resolution, minimum 0, of a cell
        :return: the width of a cell of said refinement.
        """
        assert refinement >= 0
        return self.Ratio * (pi / 2) * self.N_side ** (-refinement)

    def rowcol(self, cell):
        """
        :param cell: cell identifier, of type CellId
        :return: row_id and col_id of a cell
        """
        # Given a letter, let its row and column ID be the letter itself
        row_id = [cell.value[0]]
        col_id = [cell.value[0]]

        for c in cell.value[1:]:
            row, col = self.rowcol_cells[int(c)]
            row_id.append(row)
            col_id.append(col)

        return row_id, col_id

    def up(self, cell1, cell2):
        """
        :param cell1: cell identifier, of type CellId
        :param cell2: cell identifier, of type CellId
        :return: True if cell1 is above cell2, False if not.
        """
        cell1_row, cell1_col = self.rowcol(cell1)
        cell2_row, cell2_col = self.rowcol(cell2)
        result = True
        finish = False
        index = 1
        if self.coords_R0[cell1_row[0]][0] < self.coords_R0[cell2_row[0]][0]:
            result = True
            finish = True
        elif self.coords_R0[cell1_row[0]][0] > self.coords_R0[cell2_row[0]][0]:
            result = False
            finish = True

        while not finish and len(cell1_row) > 1 and len(cell2_row) > 1:
            if cell1_row[index] < cell2_row[index]:
                finish = True
                result = True
            elif cell1_row[index] > cell2_row[index]:
                finish = True
                result = False
            elif index == len(cell1_row) - 1 or index == len(cell2_row) - 1:
                if len(cell1_row) > len(cell2_row):
                    result = False
                else:
                    result = True
                finish = True
            index = index + 1
        return result

    def down(self, cell1, cell2):
        """
        :param cell1: cell identifier, of type CellId
        :param cell2: cell identifier, of type CellId
        :return: True if cell cell1 is below cell2, False if not.
        """
        cell1_row, cell1_col = self.rowcol(cell1)
        cell2_row, cell2_col = self.rowcol(cell2)
        result = True
        finish = False
        index = 1
        if self.coords_R0[cell1_row[0]][0] > self.coords_R0[cell2_row[0]][0]:
            result = True
            finish = True
        elif self.coords_R0[cell1_row[0]][0] < self.coords_R0[cell2_row[0]][0]:
            result = False
            finish = True

        while not finish and len(cell1_row) > 1 and len(cell2_row) > 1:
            if cell1_row[index] > cell2_row[index]:
                finish = True
                result = True
            elif cell1_row[index] < cell2_row[index]:
                finish = True
                result = False
            elif index == len(cell1_row) - 1 or index == len(cell2_row) - 1:
                if len(cell1_row) > len(cell2_row):
                    result = False
                else:
                    result = True
                finish = True

            index = index + 1
        return result

    def left(self, cell1, cell2):
        """
        :param cell1: cell identifier, of type CellId
        :param cell2: cell identifier, of type CellId
        :return: True if cell cell1 is to the left of cell cell2, False if not.
        """
        cell1_row, cell1_col = self.rowcol(cell1)
        cell2_row, cell2_col = self.rowcol(cell2)
        result = True
        finish = False
        index = 1
        if self.coords_R0[cell1_row[0]][1] < self.coords_R0[cell2_row[0]][1]:
            result = True
            finish = True
        elif self.coords_R0[cell1_row[0]][1] > self.coords_R0[cell2_row[0]][1]:
            result = False
            finish = True

        while not finish and len(cell1_col) > 1 and len(cell2_col) > 1:
            if cell1_col[index] < cell2_col[index]:
                finish = True
                result = True
            elif cell1_col[index] > cell2_col[index]:
                finish = True
                result = False
            elif index == len(cell1_col) - 1 or index == len(cell2_col) - 1:
                if len(cell1_col) > len(cell2_col):
                    result = False
                else:
                    result = True
                finish = True
            index = index + 1
        return result

    def right(self, cell1, cell2):
        """
        :param cell1: cell identifier, of type CellId
        :param cell2: cell identifier, of type CellId
        :return: True if cell cell1 is to the right of cell cell2, False if not.
        """
        cell1_row, cell1_col = self.rowcol(cell1)
        cell2_row, cell2_col = self.rowcol(cell2)
        result = True
        finish = False
        index = 1
        if self.coords_R0[cell1_row[0]][1] > self.coords_R0[cell2_row[0]][1]:
            result = True
            finish = True
        elif self.coords_R0[cell1_row[0]][1] < self.coords_R0[cell2_row[0]][1]:
            result = False
            finish = True

        while not finish and len(cell1_col) > 1 and len(cell2_col) > 1:
            if cell1_col[index] > cell2_col[index]:
                finish = True
                result = True
            elif cell1_col[index] < cell2_col[index]:
                finish = True
                result = False
            elif index == len(cell1_col) - 1 or index == len(cell2_col) - 1:
                if len(cell1_col) > len(cell2_col):
                    result = False
                else:
                    result = True
                finish = True
            index = index + 1
        return result

    def round_coord(self, value, decimals, up):
        """
        :param value: value of the real number that you want to round
        :param decimals: number of decimals to round
        :param up: if True, rounds upward, if False rounds downward
        :return: rounded real number
        """
        with decimal.localcontext() as ctx:
            d = decimal.Decimal(value)
            if value < 0:
                up = not up
            if up:
                ctx.rounding = decimal.ROUND_UP
            else:
                ctx.rounding = decimal.ROUND_DOWN
            return round(d, decimals)

    def check_bounds(self, bounds):
        """
        :param bounds: list of vertices (x,y) of a bounding box (projected coordinates)
         [upper left, upper right, lower left, lower right]
        :return: True if none of the vertices of the bounding box are outside the unfolded cube polygon.
        False if any of the vertices of the bounding box are outside the polygon, that is, it is not a correct
        projected point.
        """
        round_up_x = True
        round_up_y = False
        i = 0
        for point in bounds:
            point = Point(self.round_coord(point[0], 8, round_up_x),
                          self.round_coord(point[1], 8, round_up_y))
            if not self.polygon.contains(point):
                return False
            round_up_x = not round_up_x
            i = i + 1
            if i == 2:
                round_up_y = not round_up_y
        return True

    def get_cell_ul_vertex(self, cell):
        """
        :param cell: cell identifier, of type CellId
        :return: the top left vertex (x,y) of the cell (projected coordinates)
        """
        refinement = cell.get_refinement()

        # Coordinates of the refinement 0 cell containing cell.
        x0, y0 = self.R0_ul_vertex.get(cell.value[0])

        # Distances between the ul_vertex of refinement 0 cell and the ul_vertex of cell
        # as fractions of the width of refinement 0 cell.
        row_id, col_id = self.rowcol(cell)
        dx = sum(self.N_side ** (-i) * col_id[i]
                for i in range(1, refinement + 1))
        dy = sum(self.N_side ** (-i) * row_id[i]
                for i in range(1, refinement + 1))

        # Coordinates of the ul_vertex of cell.
        x = x0 + self.cell_width(0) * dx
        y = y0 - self.cell_width(0) * dy

        return x, y

    def get_cell_projected_coordinates(self, cell):
        """
        :param cell: cell identifier, of type CellId
        :return: projected coordinates of the vertices of the cell
        [upper left, upper right, lower left, lower right, nucleus]
        """
        w = self.cell_width(cell.get_refinement())
        ul = self.get_cell_ul_vertex(cell)
        ur = (ul[0] + w, ul[1])
        dr = (ul[0] + w, ul[1] - w)
        dl = (ul[0], ul[1] - w)
        nucleus = (ul[0] + w / 2, ul[1] - w / 2)

        return ul, ur, dl, dr, nucleus

    def get_cell_geodetic_coordinates(self, cell):
        """
        :param cell: cell identifier, of type CellId
        :return: geodetic coordinates of the vertices of the cell with id cell_id
                [upper left, upper right, lower left, lower right, nucleus]
        """
        projected_coordinates = self.get_cell_projected_coordinates(cell)
        geodetic_coordinate = []
        round_up_x = True
        round_up_y = False
        i = 0
        for coord in projected_coordinates:
            geodetic_coordinate.append(
                self.proj(self.round_coord(coord[0], 8, round_up_x), self.round_coord(coord[1], 8, round_up_y),
                          inverse=True))
            round_up_x = not round_up_x
            i = i + 1
            if i == 2:
                round_up_y = not round_up_y
        return geodetic_coordinate

    def get_geodetic_coordinates_from_bbox(self, bounds):
        """
        :param bounds: list of vertices (x,y) of the bounding box
        :return: geodetic coordinates from the points, bounds, that define a bounding box.
                (upper left, upper right, lower left, lower right, nucleus)
        """
        geodetic_coordinate = []
        round_up_x = True
        round_up_y = False
        i = 0
        for coord in bounds:
            geodetic_coordinate.append(
                list(self.proj(self.round_coord(coord[0], 8, round_up_x), self.round_coord(coord[1], 8, round_up_y),
                       inverse=True)))
            round_up_x = not round_up_x
            i = i + 1
            if i == 2:
                round_up_y = not round_up_y
        return geodetic_coordinate

    def get_c0_contains_p(self, point):
        """
        :param point: coordinates (x, y) of a point
        :return: identifier of cell of refinement 0 that point lies in
        """
        ns = self.north_square
        ss = self.south_square
        R = self.Ratio

        x, y = point

        limits = {
            'N': ((R * pi / 4, R * 3 * pi / 4), (R * (-pi + ns * (pi / 2)), R * (-pi / 2 + ns * (pi / 2)))),
            'O': ((-R * pi / 4, R * pi / 4), (-R * pi, -R * pi / 2)),
            'P': ((-R * pi / 4, R * pi / 4), (-R * pi / 2, 0)),
            'Q': ((-R * pi / 4, R * pi / 4), (0, R * pi / 2)),
            'R': ((-R * pi / 4, R * pi / 4), (R * pi / 2, R * pi)),
            'S': ((-R * 3 * pi / 4, -R * pi / 4), (R * (-pi + ss * (pi / 2)), R * (-pi / 2 + ss * (pi / 2))))
        }

        if limits['N'][0][0] < y < limits['N'][0][1] and \
                limits['N'][1][0] < x < limits['N'][1][1]:
            c0 = self.cells_R0[0]
        elif limits['S'][0][0] < y < limits['S'][0][1] and \
                limits['S'][1][0] < x < limits['S'][1][1]:
            c0 = self.cells_R0[5]
        elif limits['O'][0][0] < y < limits['O'][0][1] and \
                limits['O'][1][0] < x < limits['O'][1][1]:
            c0 = self.cells_R0[1]
        elif limits['P'][0][0] < y < limits['P'][0][1] and \
                limits['P'][1][0] < x < limits['P'][1][1]:
            c0 = self.cells_R0[2]
        elif limits['Q'][0][0] < y < limits['Q'][0][1] and \
                limits['Q'][1][0] < x < limits['Q'][1][1]:
            c0 = self.cells_R0[3]
        elif limits['R'][0][0] < y < limits['R'][0][1] and \
                limits['R'][1][0] < x < limits['R'][1][1]:
            c0 = self.cells_R0[4]
        else:
            return None

        return c0

    def get_cell_from_point(self, refinement, point):
        """
        :param refinement: the refinement, minimum 0, of a cell
        :param point: coordinates (x, y) of a point
        :return: CellId containing the point
        """
        assert refinement >= 0

        x0, y0 = point  # geodetic coordinates (HEALPix)
        x, y = self.proj(round(x0, 8), round(y0, 8))  # projected coordinates (rHEALPix)

        # Given a point (x,y) in the rHEALPix planar image and an integer i ≥
        # 0, we can compute the ID of the refinement i cell that contains (x, y) as follows.
        #
        # First compute the refinement 0 cell containing (x, y).
        cell = self.get_c0_contains_p((x, y))
        if refinement == 0:
            return CellID(cell)

        # Then compute the horizontal and vertical distances from (x, y) to ul(cell):
        dx = abs(self.R0_ul_vertex[cell][0] - x)
        dy = abs(self.R0_ul_vertex[cell][1] - y)

        if dx == 1:
            dx = dx - (0.5 * self.cell_width(self.max_refinement))
        if dy == 1:
            dy = dy - (0.5 * self.cell_width(self.max_refinement))

        # Then find out how far along the width w = Rqπ/2 of cell lie dx and dy by computing
        # the base Nside expansions (0.s)Nside and (0.t)Nside of dx/(Rπ/2) and dy/(Rπ/2), respectively.
        #
        # Truncating s and t at i digits then gives the column and row IDs, respectively,
        # of the refinement i cell containing (x, y):

        w = self.cell_width(0)
        n_cells = self.N_side ** refinement

        row_id = base_repr(math.trunc(dy / w * n_cells), self.N_side)
        col_id = base_repr(math.trunc(dx / w * n_cells), self.N_side)

        # Set the amount of zeros according to the refinement
        row_id = '0' * (refinement - len(row_id)) + row_id
        col_id = '0' * (refinement - len(col_id)) + col_id

        # Use the col and row IDs of cell to get the cell_id.
        for i in range(refinement):
            cell = cell + str(self.rowcol_cells[(int(row_id[i]), int(col_id[i]))])
        return CellID(cell)
