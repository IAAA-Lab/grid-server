import unittest
from numpy import pi

from dggs.cell_ID import CellID
from dggs.rHealPix import rHEALPix

r = rHEALPix(N_side=3, north_square=0, south_square=0)


class TestBoundaryDataSet(unittest.TestCase):

    def test_cell_width(self):
        self.assertEqual(r.cell_width(0), 0.998882147091 * (pi / 2) * 3 ** (-0))
        self.assertEqual(r.cell_width(10), 0.998882147091 * (pi / 2) * 3 ** (-10))

    def test_rowcol(self):
        self.assertEqual(r.rowcol(CellID('N00')), (['N', 0, 0], ['N', 0, 0]))
        self.assertEqual(r.rowcol(CellID('O4')), (['O', 1], ['O', 1]))
        self.assertEqual(r.rowcol(CellID('S800')), (['S', 2, 0, 0], ['S', 2, 0, 0]))

    def test_up_down(self):
        self.assertEqual(r.up(CellID('N00'), CellID('O00')), True)
        self.assertEqual(r.down(CellID('S80'), CellID('P3')), True)
        self.assertEqual(r.up(CellID('O00'), CellID('N00')), False)
        self.assertEqual(r.down(CellID('P3'), CellID('S80')), False)

    def test_right_left(self):
        self.assertEqual(r.left(CellID('N00'), CellID('O80')), True)
        self.assertEqual(r.right(CellID('R3'), CellID('P5')), True)
        self.assertEqual(r.left(CellID('O80'), CellID('N00')), False)
        self.assertEqual(r.right(CellID('P3'), CellID('R5')), False)

    def test_check_bounds(self):
        self.assertEqual(
            r.check_bounds([(-3 / 4 * pi, 1 / 8 * pi), (-1 / 2 * pi, 1 / 8 * pi), (-3 / 4 * pi, -1 / 8 * pi),
                            (-1 / 2 * pi, -1 / 8 * pi)]), True)
        self.assertEqual(r.check_bounds([(-1 / 4 * pi, 1 / 2 * pi), (0, 1 / 2 * pi), (-1 / 4 * pi, 1 / 4 * pi),
                                         (0 * pi, 1 / 4 * pi)]), False)

    def test_cell_ul_vertex(self):
        self.assertEqual(r.get_cell_ul_vertex(CellID('N0')),
                         ((-pi + 0 * pi / 2) * 0.998882147091, (3 * pi / 4) * 0.998882147091))
        self.assertEqual(r.get_cell_ul_vertex(CellID('S0')),
                         ((-pi + 0 * pi / 2) * 0.998882147091, (-pi / 4) * 0.998882147091))
        self.assertEqual(r.get_cell_ul_vertex(CellID('P')), ((-pi / 2) * 0.998882147091, (pi / 4) * 0.998882147091))
        self.assertEqual(r.get_cell_ul_vertex(CellID('O123')), (-2.266391699796672, 0.726407596088677))

    def test_cell_projected_coordinates(self):
        a = r.get_cell_projected_coordinates(CellID('N'))
        b = ((-3.1380808151030846, 2.3535606113273135), (-1.5690404075515423, 2.3535606113273135),
             (-3.1380808151030846, 0.7845202037757713), (-1.5690404075515423, 0.7845202037757713),
             (-2.3535606113273135, 1.5690404075515425))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('O'))
        b = ((-3.1380808151030846, 0.7845202037757711), (-1.5690404075515423, 0.7845202037757711),
             (-3.1380808151030846, -0.7845202037757711), (-1.5690404075515423, -0.7845202037757711),
             (-2.3535606113273135, 0.0))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('P'))
        b = ((-1.5690404075515423, 0.7845202037757711), (0.0, 0.7845202037757711),
             (-1.5690404075515423, -0.7845202037757711), (0.0, -0.7845202037757711),
             (-0.7845202037757711, 0.0))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('Q'))
        b = ((0.0, 0.7845202037757711), (1.5690404075515423, 0.7845202037757711),
             (0.0, -0.7845202037757711), (1.5690404075515423, -0.7845202037757711),
             (0.7845202037757711, 0.0))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('R'))
        b = ((1.5690404075515423, 0.7845202037757711), (3.1380808151030846, 0.7845202037757711),
             (1.5690404075515423, -0.7845202037757711), (3.1380808151030846, -0.7845202037757711),
             (2.3535606113273135, 0.0))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('S'))
        b = ((-3.1380808151030846, -0.7845202037757711), (-1.5690404075515423, -0.7845202037757711),
             (-3.1380808151030846, -2.3535606113273135), (-1.5690404075515423, -2.3535606113273135),
             (-2.3535606113273135, -1.5690404075515423))
        self.assertEqual(a, b)

        a = r.get_cell_projected_coordinates(CellID('N88'))
        b = ((-1.743378230612825, 0.9588580268370539),
             (-1.5690404075515425, 0.9588580268370539),
             (-1.743378230612825, 0.7845202037757715),
             (-1.5690404075515425, 0.7845202037757715),
             (-1.6562093190821836, 0.8716891153064127))
        self.assertEqual(a, b)

    def test_cell_geodetic_coordinates(self):
        a = r.get_cell_geodetic_coordinates(CellID('N'))
        b = [(89.99999978400184, 41.93785398898271), (6.72073022798356e-08, 41.93785398898271),
             (179.99999993279272, 41.93785423508538), (-89.99999978400186, 41.93785406555696),
             (21.357842301203913, 90.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('O'))
        b = [(-179.9999997096064, 41.93785365811587), (-90.00000014160271, 41.93785365811587),
             (-179.9999997096064, -41.93785365811587), (-90.00000014160271, -41.93785365811587),
             (-134.99999992560458, 0.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('P'))
        b = [(-89.99999956800372, 41.93785365811587), (0.0, 41.93785365811587),
             (-89.99999956800372, -41.93785365811587), (0.0, -41.93785365811587),
             (-44.99999978400186, 0.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('Q'))
        b = [(0.0, 41.93785365811587), (89.99999956800372, 41.93785365811587),
             (0.0, -41.93785365811587), (89.99999956800372, -41.93785365811587),
             (45.000000357600854, 0.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('R'))
        b = [(90.00000014160271, 41.93785365811587), (179.9999997096064, 41.93785365811587),
             (90.00000014160271, -41.93785365811587), (179.9999997096064, -41.93785365811587),
             (135.00000049920357, 0.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('S'))
        b = [(179.99999993279272, -41.93785423508538), (-89.99999978400186, -41.93785406555696),
             (89.99999978400184, -41.93785398898271), (6.72073022798356e-08, -41.93785398898271),
             (-127.2504110460384, -90.0)]
        self.assertEqual(a, b)

        a = r.get_cell_geodetic_coordinates(CellID('N88'))
        b = [(-90.00000045977251, 53.09647087781202),
             (-80.00000050159962, 41.93785406555696),
             (-99.99999968800269, 41.93785431165961),
             (-89.99999978400186, 41.93785406555696),
             (-89.99999911170322, 47.57255041493694)]
        self.assertEqual(a, b)

    def test_cell_from_point(self):
        p = (43.74999986695531, 47.57255097966877)
        cell = r.get_cell_from_point(4, p)
        self.assertEqual(cell, CellID('N1145'))

        p2 = (54.00000032594864, 54.91640765274602)
        cell = r.get_cell_from_point(3, p2)
        self.assertEqual(cell, CellID('N132'))

        p3 = (-133.74999985810513, -47.57255129550154)
        cell = r.get_cell_from_point(5, p3)
        self.assertEqual(cell, CellID('S11454'))

        p4 = (-134.38356121039018, -46.9523050079352)
        cell = r.get_cell_from_point(7, p4)
        self.assertEqual(cell, CellID('S1145000'))

        p5 = (-1.1179698216735403, 41.82074068655)
        cell = r.get_cell_from_point(2, p5)
        self.assertEqual(cell, CellID('P22'))


if __name__ == '__main__':
    unittest.main()
