from pymongo import MongoClient
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.boundary_store import BoundaryStore
from dggs.data import Data

store = BoundaryStore(MongoClient(port=27017).bds)


def test_insert():
    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('N0')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('N8O2P0')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('O6S0S1S2')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('Q')), Data(""))
    store.insert(bds)
    store.dropAll()


def test_query_by_boundary():
    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    store.insert(bds)

    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('R1R2')), Data(""))
    store.insert(bds)

    store.query_by_boundary(Boundary(boundary_ID=BoundaryID('P12P34O23S56')))

    store.dropAll()


def test_query_by_polygon():
    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('R0')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('O2P0')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('S0S1')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('Q')), Data(""))
    store.insert(bds)

    b = Boundary(boundary_ID=BoundaryID('O0O1O2'))
    polygon = b.get_bbox()
    store.query_by_polygon(polygon)

    b = Boundary(boundary_ID=BoundaryID('P10P11P2'))
    polygon = b.get_bbox()
    store.query_by_polygon(polygon)

    b = Boundary(boundary_ID=BoundaryID('O'))
    polygon = b.get_bbox()
    store.query_by_polygon(polygon)

    store.dropAll()


def test_delete():
    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    store.insert(bds)

    bds = BoundaryDataSet()
    bds.add(Boundary(boundary_ID=BoundaryID('P12P34O23S56')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('P10P11P2')), Data(""))
    bds.add(Boundary(boundary_ID=BoundaryID('R1R2')), Data(""))
    store.insert(bds)

    store.query_by_boundary(Boundary(boundary_ID=BoundaryID('P12P34O23S56')))
    store.delete(Boundary(boundary_ID=BoundaryID('P12P34O23S56')))
    store.query_by_boundary(Boundary(boundary_ID=BoundaryID('P12P34O23S56')))

    store.dropAll()


if __name__ == "__main__":
    test_insert()
    test_query_by_polygon()
    test_delete()
    test_query_by_boundary()
