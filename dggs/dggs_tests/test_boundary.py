import unittest
from dggs.boundary_ID import BoundaryID, AUID
from dggs.cell_ID import CellID
from dggs.cellset.boundary import Boundary, OptimalBoundary


class TestBoundary(unittest.TestCase):

    def test_boundary_from_boundary_ID(self):
        boundary = Boundary(boundary_ID=BoundaryID('N11N12N13N88O0P123S34567'))
        self.assertEqual(boundary.cells,
                         [CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88'), CellID('O0'), CellID('P123'),
                          CellID('S34567')])

    def test_boundary_from_cells(self):
        boundary = Boundary(cells=[CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88'), CellID('O0'),
                                   CellID('P123'), CellID('S34567')])
        self.assertEqual(boundary.boundary_ID.value, 'N11N12N13N88O0P123S34567')

    def test_grid_stack(self):
        boundary = Boundary(cells=[CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88'), CellID('O0'),
                                   CellID('P123'), CellID('S34567')])
        grid_stack = boundary.get_as_grid_stack()

        self.assertEqual(grid_stack.grids.__len__(), 4)

        self.assertEqual(grid_stack.grids[0].refinement_level, 1)
        self.assertEqual(grid_stack.grids[0].cells, [CellID('O0')])

        self.assertEqual(grid_stack.grids[1].refinement_level, 2)
        self.assertEqual(grid_stack.grids[1].cells, [CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88')])

        self.assertEqual(grid_stack.grids[2].refinement_level, 3)
        self.assertEqual(grid_stack.grids[2].cells, [CellID('P123')])

        self.assertEqual(grid_stack.grids[3].refinement_level, 5)
        self.assertEqual(grid_stack.grids[3].cells, [CellID('S34567')])

    def test_min_refinement(self):
        boundary = Boundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        min_refinement = boundary.get_min_refinement()
        self.assertEqual(min_refinement, 0)

    def test_max_refinement(self):
        boundary = Boundary(cells=[CellID('N'), CellID('O0'), CellID('P123'), CellID('S34567')])
        max_refinement = boundary.get_max_refinement()
        self.assertEqual(max_refinement, 5)

    def test_optimal_boundary_from_cells(self):
        optimal_boundary = OptimalBoundary(
            cells=[CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88'), CellID('O0'), CellID('P123'),
                   CellID('S34567')])
        self.assertEqual(optimal_boundary.boundary_ID.value, 'RN11$))2$))3$)))88$))))O0$)))P123$)))))S34567$))))))))')

    def test_optimal_boundary_from_AUID(self):
        optimal_boundary = OptimalBoundary(boundary_ID=AUID('RN11$))2$))3$)))88$))))O0$)))P123$)))))S34567$))))))))'))
        self.assertEqual(optimal_boundary.cells,
                         [CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88'), CellID('O0'),
                          CellID('P123'), CellID('S34567')])

    def test_optimize_boundary(self):
        boundary = Boundary(boundary_ID=BoundaryID('N11N12N2N3'))
        optimal_boundary = boundary.optimize()
        self.assertEqual(optimal_boundary.boundary_ID.value, "RN11$))2$)))2$))3$))))")
        self.assertEqual(optimal_boundary.is_optimal(), True)

        boundary = Boundary(boundary_ID=BoundaryID('N11N20N21N22N23N24N25N26N27N28'))
        self.assertEqual(boundary.boundary_ID.value, "N11N20N21N22N23N24N25N26N27N28")
        self.assertEqual(boundary.is_optimal(), False)
        optimal_boundary = boundary.optimize()
        self.assertEqual(optimal_boundary.boundary_ID.value, "RN11$)))2$))))")
        self.assertEqual(optimal_boundary.is_optimal(), True)

        boundary = Boundary(boundary_ID=BoundaryID(
            'N7N00N01N02N03N04N05N06N07N08N11N21N22N23N24N25N26N27N28N200N201N202N203N204N205N206N207N208N9878'))
        optimal_boundary = boundary.optimize()
        self.assertEqual(optimal_boundary.boundary_ID.value, "RN0$))11$)))2$))7$))9878$)))))))")
        self.assertEqual(optimal_boundary.is_optimal(), True)

    def test_boundary_projected_coordinates(self):
        boundary = Boundary(cells=[CellID('N')])
        a = boundary.get_projected_coordinates()
        b = [((-3.1380808151030846, 2.3535606113273135), (-1.5690404075515423, 2.3535606113273135),
              (-3.1380808151030846, 0.7845202037757713), (-1.5690404075515423, 0.7845202037757713),
              (-2.3535606113273135, 1.5690404075515425))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('O')])
        a = boundary.get_projected_coordinates()
        b = [((-3.1380808151030846, 0.7845202037757711), (-1.5690404075515423, 0.7845202037757711),
              (-3.1380808151030846, -0.7845202037757711), (-1.5690404075515423, -0.7845202037757711),
              (-2.3535606113273135, 0.0))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('P')])
        a = boundary.get_projected_coordinates()
        b = [((-1.5690404075515423, 0.7845202037757711), (0.0, 0.7845202037757711),
              (-1.5690404075515423, -0.7845202037757711), (0.0, -0.7845202037757711),
              (-0.7845202037757711, 0.0))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('Q')])
        a = boundary.get_projected_coordinates()
        b = [((0.0, 0.7845202037757711), (1.5690404075515423, 0.7845202037757711),
              (0.0, -0.7845202037757711), (1.5690404075515423, -0.7845202037757711),
              (0.7845202037757711, 0.0))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('R')])
        a = boundary.get_projected_coordinates()
        b = [((1.5690404075515423, 0.7845202037757711), (3.1380808151030846, 0.7845202037757711),
              (1.5690404075515423, -0.7845202037757711), (3.1380808151030846, -0.7845202037757711),
              (2.3535606113273135, 0.0))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('S')])
        a = boundary.get_projected_coordinates()
        b = [((-3.1380808151030846, -0.7845202037757711), (-1.5690404075515423, -0.7845202037757711),
              (-3.1380808151030846, -2.3535606113273135), (-1.5690404075515423, -2.3535606113273135),
              (-2.3535606113273135, -1.5690404075515423))]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88')])
        a = boundary.get_projected_coordinates()
        b = [((-2.440729522857955, 2.3535606113273135), (-2.266391699796672, 2.3535606113273135),
              (-2.440729522857955, 2.179222788266031), (-2.266391699796672, 2.179222788266031),
              (-2.3535606113273135, 2.266391699796672)), ((-2.266391699796672, 2.3535606113273135),
                                                          (-2.0920538767353896, 2.3535606113273135),
                                                          (-2.266391699796672, 2.179222788266031),
                                                          (-2.0920538767353896, 2.179222788266031),
                                                          (-2.179222788266031, 2.266391699796672)),
             ((-2.615067345919237, 2.179222788266031), (-2.4407295228579544, 2.179222788266031),
              (-2.615067345919237, 2.0048849652047482), (-2.4407295228579544, 2.0048849652047482),
              (-2.5278984343885957, 2.0920538767353896)), ((-1.743378230612825, 0.9588580268370539),
                                                           (-1.5690404075515425, 0.9588580268370539),
                                                           (-1.743378230612825, 0.7845202037757715),
                                                           (-1.5690404075515425, 0.7845202037757715),
                                                           (-1.6562093190821836, 0.8716891153064127))]
        self.assertEqual(a, b)

    def test_boundary_geodetic_coordinates(self):
        boundary = Boundary(cells=[CellID('N')])
        a = boundary.get_geodetic_coordinates()
        b = [[(89.99999978400184, 41.93785398898271), (6.72073022798356e-08, 41.93785398898271),
              (179.99999993279272, 41.93785423508538), (-89.99999978400186, 41.93785406555696),
              (21.357842301203913, 90.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('O')])
        a = boundary.get_geodetic_coordinates()
        b = [[(-179.9999997096064, 41.93785365811587), (-90.00000014160271, 41.93785365811587),
              (-179.9999997096064, -41.93785365811587), (-90.00000014160271, -41.93785365811587),
              (-134.99999992560458, 0.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('P')])
        a = boundary.get_geodetic_coordinates()
        b = [[(-89.99999956800372, 41.93785365811587), (0.0, 41.93785365811587),
              (-89.99999956800372, -41.93785365811587), (0.0, -41.93785365811587),
              (-44.99999978400186, 0.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('Q')])
        a = boundary.get_geodetic_coordinates()
        b = [[(0.0, 41.93785365811587), (89.99999956800372, 41.93785365811587),
              (0.0, -41.93785365811587), (89.99999956800372, -41.93785365811587),
              (45.000000357600854, 0.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('R')])
        a = boundary.get_geodetic_coordinates()
        b = [[(90.00000014160271, 41.93785365811587), (179.9999997096064, 41.93785365811587),
              (90.00000014160271, -41.93785365811587), (179.9999997096064, -41.93785365811587),
              (135.00000049920357, 0.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('S')])
        a = boundary.get_geodetic_coordinates()
        b = [[(179.99999993279272, -41.93785423508538), (-89.99999978400186, -41.93785406555696),
              (89.99999978400184, -41.93785398898271), (6.72073022798356e-08, -41.93785398898271),
              (-127.2504110460384, -90.0)]]
        self.assertEqual(a, b)

        boundary = Boundary(cells=[CellID('N11'), CellID('N12'), CellID('N13'), CellID('N88')])
        a = boundary.get_geodetic_coordinates()
        b = [[(49.99999984613771, 41.93785398898271), (40.00000000507141, 41.93785398898271),
              (51.42857120155658, 53.09647119578482), (38.57142860714087, 53.09647119578482),
              (44.99999991630516, 47.57255097966877)], [(39.99999943147242, 41.93785398898271),
                                                        (30.000000164005154, 41.93785398898271),
                                                        (38.57142786965645, 53.09647119578482),
                                                        (25.714286012725182, 53.09647119578482),
                                                        (33.74999947215674, 47.57255097966877)],
             [(64.28571411203704, 53.096471823859616), (51.42857204439592, 53.096471823859616),
              (71.9999990936704, 63.883501580904124), (54.00000064109378, 63.883501580904124),
              (59.99999953080601, 58.528017276850065)], [(-90.00000045977251, 53.09647087781202),
                                                         (-80.00000050159962, 41.93785406555696),
                                                         (-99.99999968800269, 41.93785431165961),
                                                         (-89.99999978400186, 41.93785406555696),
                                                         (-89.99999911170322, 47.57255041493694)]]

        self.assertEqual(a, b)

    def test_bbox(self):
        boundary = Boundary(boundary_ID=BoundaryID('O0O1O3O4'))
        bbox = [[[-179.9999997096064, -12.895312716341486], [-120.00000018880363, -12.895312716341486],
                 [-120.00000018880363, 41.93785365811587], [-179.9999997096064, 41.93785365811587],
                 [-179.9999997096064, -12.895312716341486]]]
        self.assertEqual(boundary.get_bbox(), bbox)

        boundary = Boundary(boundary_ID=BoundaryID('O0O1O3'))
        bbox = [[[-179.9999997096064, -12.895312716341486], [-120.00000018880363, -12.895312716341486],
                 [-120.00000018880363, 41.93785365811587], [-179.9999997096064, 41.93785365811587],
                 [-179.9999997096064, -12.895312716341486]]]
        self.assertEqual(boundary.get_bbox(), bbox)

        boundary = Boundary(boundary_ID=BoundaryID('O1O3O4'))
        bbox = [[[-179.9999997096064, -12.895312716341486], [-120.00000018880363, -12.895312716341486],
                 [-120.00000018880363, 41.93785365811587], [-179.9999997096064, 41.93785365811587],
                 [-179.9999997096064, -12.895312716341486]]]
        self.assertEqual(boundary.get_bbox(), bbox)

        boundary = Boundary(boundary_ID=BoundaryID('O0O4'))
        bbox = [[[-179.9999997096064, -12.895312716341486], [-120.00000018880363, -12.895312716341486],
                 [-120.00000018880363, 41.93785365811587], [-179.9999997096064, 41.93785365811587],
                 [-179.9999997096064, -12.895312716341486]]]
        self.assertEqual(boundary.get_bbox(), bbox)

        boundary = Boundary(boundary_ID=BoundaryID('N5P1P2'))
        bbox = [[[-89.99999763120867, 12.895313217732834], [-5.735989944427416e-07, 12.895313217732834],
                 [-5.735989944427416e-07, 74.42400629900254], [-89.99999763120867, 74.42400629900254],
                 [-89.99999763120867, 12.895313217732834]]]
        self.assertEqual(boundary.get_bbox(), bbox)

        boundary = Boundary(boundary_ID=BoundaryID('Q6Q7S7'))
        bbox = [[[1.9224187603958446e-06, -74.4240062287476], [89.9999976312087, -74.4240062287476],
                 [89.9999976312087, -12.895313217732834], [1.9224187603958446e-06, -12.895313217732834],
                 [1.9224187603958446e-06, -74.4240062287476]]]
        self.assertEqual(boundary.get_bbox(), bbox)

    def test_limit_cells(self):
        boundary = Boundary(cells=[CellID('N1'), CellID('O0'), CellID('P123'), CellID('S34567')])
        top_cell, bottom_cell, left_cell, right_cell = boundary.get_limit_cells()

        self.assertEqual(top_cell, CellID('N1'))
        self.assertEqual(bottom_cell, CellID('S34567'))
        self.assertEqual(left_cell, CellID('O0'))
        self.assertEqual(right_cell, CellID('P123'))


if __name__ == '__main__':
    unittest.main()
