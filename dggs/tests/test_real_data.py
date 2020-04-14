import json
import fiona
from pymongo import MongoClient
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_store import BoundaryStore
from dggs.rHealPix import rHEALPix
import requests


class ShpFile:

    def __init__(self, file, dggs=None):
        self.file = file
        self.shapes = fiona.open(file)
        if dggs is None:
            dggs = rHEALPix(N_side=3, north_square=0, south_square=0)
        self.dggs = dggs

    def test_API(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        i = 0
        data = {}
        bds = []
        boundary_id = ''
        bds_test = []
        boundary_test = []
        test_boundary_id = ''

        for polygon in self.shapes:
            if i % 10 == 0 and i != 0:
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                test_boundary_id = boundary_id
                boundary_test = [{'boundary': optB.boundary_ID.value, 'data': data}]
                data = {}
                boundary_id = ''
            boundary_id = boundary_id + polygon['properties']['id']
            data[polygon['properties']['id']] = polygon['properties']
            i = i + 1
        boundary_dataset = {'boundary_data_set': bds}
        boundary_dataset_test = {'boundary_data_set': bds_test}

        # POST BOUNDARY_DATASETS TEST
        r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
        assert r.status_code == 201

        # GET ALL BOUNDARY_DATASETS TEST
        r = requests.get('http://127.0.0.1:8000/bdatasets/' + test_boundary_id)
        json_test = json.dumps([boundary_dataset_test])
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # GET BOUNDARY IN BOUNDARY_DATASET TEST
        r = requests.get('http://127.0.0.1:8000/bdatasets/')
        json_test = json.dumps([boundary_dataset_test])
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # GET ALL BOUNDARIES TEST
        r = requests.get('http://127.0.0.1:8000/boundaries/')
        json_test = json.dumps(bds_test)
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # GET BOUNDARY TEST
        r = requests.get('http://127.0.0.1:8000/boundaries/' + test_boundary_id)
        json_test = json.dumps(boundary_test)
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # DELETE BOUNDARY TEST
        r = requests.delete('http://127.0.0.1:8000/boundaries/' + test_boundary_id)
        assert r.status_code == 204

        r = requests.get('http://127.0.0.1:8000/boundaries/')
        bds_test.pop()
        json_test = json.dumps(bds_test)
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_08(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        i = 0
        data = {}
        bds = []
        boundary_id = ''
        bds_test = []

        for polygon in self.shapes:
            if i != 0:
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                data = {}
                boundary_id = ''
            boundary_id = boundary_id + polygon['properties']['id']
            data[polygon['properties']['id']] = polygon['properties']
            i = i + 1
        boundary_dataset = {'boundary_data_set': bds}

        # POST BOUNDARY_DATASETS TEST
        r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
        assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.9674',
            'dly': '41.6645',
            'urx': '-0.9395',
            'ury': '41.6806'
        }
        cells = [Boundary(boundary_ID=BoundaryID('P22220464')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220465')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220473')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220467')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220468')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220476')).optimize().boundary_ID.value]

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_cells = 0
        for boundary in r.json():
            assert cells.__contains__(boundary['boundary'])
            num_cells = num_cells + 1
        assert num_cells == len(cells)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_09(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        i = 0
        data = {}
        bds = []
        boundary_id = ''
        bds_test = []

        for polygon in self.shapes:
            if i != 0:
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                data = {}
                boundary_id = ''
            boundary_id = boundary_id + polygon['properties']['id']
            data[polygon['properties']['id']] = polygon['properties']
            i = i + 1
        boundary_dataset = {'boundary_data_set': bds}

        # POST BOUNDARY_DATASETS TEST
        r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
        assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.90309',
            'dly': '41.64419',
            'urx': '-0.89381',
            'ury': '41.64957'
        }
        cells = [Boundary(boundary_ID=BoundaryID('P222207203')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P222207204')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P222207205')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P222207206')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P222207207')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P222207208')).optimize().boundary_ID.value]

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_cells = 0
        for boundary in r.json():
            assert cells.__contains__(boundary['boundary'])
            num_cells = num_cells + 1
        assert num_cells == len(cells)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_10(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        i = 0
        data = {}
        bds = []
        boundary_id = ''
        bds_test = []

        for polygon in self.shapes:
            if i != 0:
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                data = {}
                boundary_id = ''
            boundary_id = boundary_id + polygon['properties']['id']
            data[polygon['properties']['id']] = polygon['properties']
            i = i + 1
        boundary_dataset = {'boundary_data_set': bds}

        # POST BOUNDARY_DATASETS TEST
        r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
        assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.90153',
            'dly': '41.64244',
            'urx': '-0.89848',
            'ury': '41.64421'
        }
        cells = [Boundary(boundary_ID=BoundaryID('P2222072065')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P2222072068')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P2222072073')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P2222072074')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P2222072076')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P2222072077')).optimize().boundary_ID.value]

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_cells = 0
        for boundary in r.json():
            assert cells.__contains__(boundary['boundary'])
            num_cells = num_cells + 1
        assert num_cells == len(cells)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_11(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        i = 0
        data = {}
        bds = []
        boundary_id = ''
        bds_test = []

        for polygon in self.shapes:
            if i != 0:
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                data = {}
                boundary_id = ''
            boundary_id = boundary_id + polygon['properties']['id']
            data[polygon['properties']['id']] = polygon['properties']
            i = i + 1
        boundary_dataset = {'boundary_data_set': bds}

        # POST BOUNDARY_DATASETS TEST
        r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
        assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.903563',
            'dly': '41.644185',
            'urx': '-0.902558',
            'ury': '41.644762'
        }
        cells = [Boundary(boundary_ID=BoundaryID('P22220720640')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220720641')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220720642')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220720643')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220720644')).optimize().boundary_ID.value,
                 Boundary(boundary_ID=BoundaryID('P22220720645')).optimize().boundary_ID.value]

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_cells = 0
        for boundary in r.json():
            assert cells.__contains__(boundary['boundary'])
            num_cells = num_cells + 1
        assert num_cells == len(cells)

        store.dropAll()

        print('TEST FINISH')


if __name__ == "__main__":
    """
    EMOCIONES
    """
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_08.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_09.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_10.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_11.shp")
    shp.test_API()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_08.shp")
    shp.test_API_polygon_08()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_09.shp")
    shp.test_API_polygon_09()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_10.shp")
    shp.test_API_polygon_10()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_EMOCIONES/MALLA_FINAL_11.shp")
    shp.test_API_polygon_11()

    """
    CARRIL BICI
    """
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_08.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_09.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_10.shp")
    shp.test_API()
    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_11.shp")
    shp.test_API()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_08.shp")
    shp.test_API_polygon_08()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_09.shp")
    shp.test_API_polygon_09()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_10.shp")
    shp.test_API_polygon_10()

    shp = ShpFile("/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/mallas_DGGS/resultados_CARRIL_BICI/BICIS_11.shp")
    shp.test_API_polygon_11()
