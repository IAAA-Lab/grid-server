import json
import fiona
from pymongo import MongoClient
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_store import BoundaryStore
import requests
import glob, os


class TestsEmocionesBoundaries:

    def __init__(self, path):
        self.path = path
        self.bds = []
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                os.chdir(path + dir)
                boundaries = []
                for file in glob.glob("MALLA*.shp"):
                    boundaries.append(fiona.open(file))
                self.bds.append(
                    {
                        'person': dir,
                        'boundaries': boundaries
                    }
                )

    def test_API(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        boundary_dataset_test = {}
        all_bds_test = []
        all_boundaries = []
        boundary_test = []
        test_boundary_id = ''
        for person in self.bds[0:10]:
            bds = []
            bds_test = []
            for boundaries in person['boundaries']:
                data = {}
                boundary_id = ''
                for polygon in boundaries:
                    boundary_id = boundary_id + polygon['properties']['id']
                    data[polygon['properties']['id']] = polygon['properties']
                bds.append({'boundary': boundary_id, 'data': data})
                optB = Boundary(boundary_ID=BoundaryID(boundary_id)).optimize()
                bds_test.append({'boundary': optB.boundary_ID.value, 'data': data})
                all_boundaries.append({'boundary': optB.boundary_ID.value, 'data': data})
                test_boundary_id = boundary_id
                boundary_test = [{'boundary': optB.boundary_ID.value, 'data': data}]
            boundary_dataset = {'boundary_data_set': bds}
            boundary_dataset_test = {'boundary_data_set': bds_test}
            all_bds_test.append(boundary_dataset_test)

            # POST BOUNDARY_DATASETS TEST
            r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
            assert r.status_code == 201

        # GET ALL BOUNDARY_DATASETS TEST
        r = requests.get('http://127.0.0.1:8000/bdatasets/')
        json_test = json.dumps(all_bds_test)
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # GET BOUNDARY IN BOUNDARY_DATASET TEST

        r = requests.get('http://127.0.0.1:8000/bdatasets/' + test_boundary_id)
        json_test = json.dumps([boundary_dataset_test])
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        # GET ALL BOUNDARIES TEST
        r = requests.get('http://127.0.0.1:8000/boundaries/')
        json_test = json.dumps(all_boundaries)
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
        all_boundaries.pop()
        json_test = json.dumps(all_boundaries)
        json_data = json.dumps(r.json())
        assert r.status_code == 200
        assert json_test == json_data

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_P03(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        for person in self.bds:
            if person['person'] == '03':
                bds = []
                for boundaries in person['boundaries']:
                    data = {}
                    boundary_id = ''
                    for polygon in boundaries:
                        boundary_id = boundary_id + polygon['properties']['id']
                        data[polygon['properties']['id']] = polygon['properties']
                    bds.append({'boundary': boundary_id, 'data': data})
                boundary_dataset = {'boundary_data_set': bds}

                # POST BOUNDARY_DATASETS TEST
                r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
                assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.903646',
            'dly': '41.665412',
            'urx': '-0.899378',
            'ury': '41.668493'
        }
        boundaries = ['RP22220486062$))5$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))160$))1$))3$))4$))5$))6$))7$))8$)))73$))4$))5$))6$))7$))8$)))83$))4$))5$))6$))7$))8$))))263$))4$))5$))6$))7$))8$)))73$))6$))))301$))2$))4$))5$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$)))40$))1$))2$))3$))4$))5$)))50$))1$))2$))3$))4$))5$))))400$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$)))72$)))80$))1$))2$))))500$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))3$))4$))6$))7$)))60$)))))7818$)))26$))7$))8$)))42$))5$)))50$))1$))2$))3$))4$))5$))8$)))))8606$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))3$))4$))5$))6$))7$))8$)))53$))4$))5$))6$))7$)))62$)))70$))1$))2$))5$)))80$))))766$)))))))722100$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))3$))4$))5$))6$))7$))8$)))32$)))40$))1$))2$)))50$))1$))2$))3$))4$))5$))))203$))4$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))7$))8$)))43$))6$))))))))))))))']

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_boundaries = 0
        for boundary in r.json():
            assert boundaries.__contains__(boundary['boundary'])
            num_boundaries = num_boundaries + 1
        assert num_boundaries == len(boundaries)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_P21(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        for person in self.bds:
            if person['person'] == '21':
                bds = []
                for boundaries in person['boundaries']:
                    data = {}
                    boundary_id = ''
                    for polygon in boundaries:
                        boundary_id = boundary_id + polygon['properties']['id']
                        data[polygon['properties']['id']] = polygon['properties']
                    bds.append({'boundary': boundary_id, 'data': data})
                boundary_dataset = {'boundary_data_set': bds}

                # POST BOUNDARY_DATASETS TEST
                r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
                assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.90267',
            'dly': '41.64054',
            'urx': '-0.89886',
            'ury': '41.64299'
        }
        boundaries = ['RP22220720638$)))46$))7$))8$)))53$))4$))5$))6$))7$))8$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))733$))4$))6$))7$))8$)))46$))7$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))3$))4$))5$))6$))7$))8$))))866$)))))3001$))2$))5$)))10$))1$))2$))3$))4$))5$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))5$))))100$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$)))30$))1$))2$))3$))4$))5$))7$))8$)))40$))1$))3$))4$))6$))))))))))))))']

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_boundaries = 0
        for boundary in r.json():
            assert boundaries.__contains__(boundary['boundary'])
            num_boundaries = num_boundaries + 1
        assert num_boundaries == len(boundaries)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_P11(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        for person in self.bds:
            if person['person'] == '11':
                bds = []
                for boundaries in person['boundaries']:
                    data = {}
                    boundary_id = ''
                    for polygon in boundaries:
                        boundary_id = boundary_id + polygon['properties']['id']
                        data[polygon['properties']['id']] = polygon['properties']
                    bds.append({'boundary': boundary_id, 'data': data})
                boundary_dataset = {'boundary_data_set': bds}

                # POST BOUNDARY_DATASETS TEST
                r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
                assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.929656',
            'dly': '41.614571',
            'urx': '-0.920650',
            'ury': '41.627084'
        }
        boundaries = ['RP22220716588$)))))7326$))7$))8$)))38$)))42$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$)))61$))2$))3$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))406$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))43$))4$))6$))7$))8$)))56$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))563$))4$))6$))7$))8$)))76$))))601$))2$)))10$))1$))2$))3$))4$))5$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))52$))))700$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$)))30$))1$))2$)))40$))))800$))1$))2$))3$))4$)))10$))1$))))))22458$)))82$))5$))8$))))533$))4$))6$))7$))8$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))70$))3$))4$))6$))7$))8$)))86$))))721$))2$))4$))5$))7$))8$)))51$))2$))3$))4$))5$))6$))7$))8$)))78$)))80$))1$))2$))3$))4$))5$))6$))))800$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$)))50$))1$))2$))3$)))60$))1$))2$)))))4115$))6$))7$))8$)))23$))4$))6$))7$))8$)))31$))2$))4$))5$)))40$))1$))2$))3$))4$))5$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$))))230$))3$))6$))7$)))60$))1$))2$)))))))800606$))))))))))))))',
                      'RP22220476527$))8$)))35$))7$))8$)))42$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$)))62$)))70$))1$))2$))3$))4$))5$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))820$))1$))2$))5$)))))7304$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))26$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))3$))6$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))3$))6$))))600$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))3$))6$)))32$)))40$))1$))2$))4$))5$)))))))708018$)))26$))7$))8$)))51$))2$))))103$))4$))5$))6$))7$))8$)))11$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$)))40$))1$))2$))4$))5$)))50$))1$))2$))3$))4$))5$))))200$))3$))4$))6$))7$)))30$))1$))2$))3$))4$))5$))8$)))43$))6$))))))20014$))5$))8$)))23$))4$))5$))6$))7$))8$)))50$))1$))2$))4$))5$))8$))))103$))4$))6$))7$))8$)))16$))7$))8$)))26$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$)))60$))1$))2$))4$))5$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))6$))))206$))7$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))3$)))60$))))410$))1$))))))))))))))',
                      'RP22220713067$))8$)))76$))7$))8$)))86$))7$))8$))))166$))7$))8$)))76$))7$))8$)))86$))7$))8$))))266$))7$))8$))))302$)))10$))1$))2$))3$))4$))5$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))42$)))50$))1$))2$))4$))5$))8$))))400$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$)))60$))1$))2$))4$))5$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))3$))))500$))1$))3$))6$))))710$))1$))2$)))))4688$))))766$))7$))8$)))74$))5$))6$))7$))8$)))83$))4$))5$))6$))7$))8$))))863$))4$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))3$)))))7100$))1$))2$))5$)))10$))1$))2$))3$))4$))5$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))51$))2$))))200$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))3$)))30$))1$))2$))4$))))))24357$))8$)))82$))))436$))7$)))60$))1$))2$))3$))4$))5$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$))8$))))560$))1$))2$))3$))4$))5$))6$))7$))8$)))73$))4$))5$))6$))7$))8$)))83$))4$))5$))6$))7$))8$))))702$)))10$))1$))2$))3$))4$))5$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))42$)))50$))1$))2$))3$))4$))5$))7$))8$)))82$))))800$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$)))60$))1$))2$))3$))4$))5$))7$)))70$))1$))2$))3$)))))5363$))4$))5$))6$))7$))8$)))73$))6$))7$))8$)))86$))))600$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$)))30$))))))))))))))']

        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_boundaries = 0
        for boundary in r.json():
            assert boundaries.__contains__(boundary['boundary'])
            num_boundaries = num_boundaries + 1
        assert num_boundaries == len(boundaries)

        store.dropAll()

        print('TEST FINISH')

    def test_API_polygon_P26(self):

        print('TEST START')
        store = BoundaryStore(MongoClient(port=27017).bds)
        store.dropAll()

        for person in self.bds:
            if person['person'] == '26':
                bds = []
                for boundaries in person['boundaries']:
                    data = {}
                    boundary_id = ''
                    for polygon in boundaries:
                        boundary_id = boundary_id + polygon['properties']['id']
                        data[polygon['properties']['id']] = polygon['properties']
                    bds.append({'boundary': boundary_id, 'data': data})
                boundary_dataset = {'boundary_data_set': bds}

                # POST BOUNDARY_DATASETS TEST
                r = requests.post('http://127.0.0.1:8000/bdatasets/', json=boundary_dataset)
                assert r.status_code == 201

        # GET BOUNDARY (POLYGON) TEST
        params = {
            'dlx': '-0.869159',
            'dly': '41.643394',
            'urx': '-0.863760',
            'ury': '41.654733'
        }
        boundaries = ['RP22220488768$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))83$))4$))6$))7$))8$)))))))722102$)))10$))1$))2$))5$)))20$))1$))2$))3$))4$))5$)))64$))5$))6$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))3$))4$))6$))7$))8$))))200$))1$))3$))4$))5$))6$))7$))8$)))13$))6$))7$))8$)))40$))1$))2$)))50$))1$))3$))4$))5$)))66$))))315$))6$))7$))8$)))21$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$)))50$))1$))2$))))400$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$)))40$))1$))2$))4$))5$)))50$))1$))2$))3$))4$))5$))))500$))1$))3$))4$))5$))6$))7$))8$)))30$))1$)))))4482$))4$))5$))7$))8$))))536$))7$)))60$))1$))2$))3$))4$))5$))6$))7$))8$)))73$))4$))6$))7$))8$))))800$))1$))2$))4$))5$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))3$))4$))5$))6$))7$))8$)))42$)))50$))1$)))))5606$)))))))800033$))6$))7$))))))))))))))',
                      'RP22220722576$))7$))8$)))83$))4$))5$))6$))7$))8$))))717$))8$)))24$))5$))6$))7$))8$)))41$))2$)))50$))1$))2$))3$))4$))5$))7$))8$)))82$))))800$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$))7$))8$)))50$))1$))2$))3$))4$))5$))6$))7$))8$)))60$))1$))2$))3$))4$))5$))7$))8$)))70$))1$))2$))3$))4$))5$))6$))7$))8$)))80$))1$))2$))3$))4$))5$))6$))7$)))))5202$)))10$))1$))2$)))))))800360$))1$))2$))3$))4$))5$))6$))7$))8$)))73$))4$))5$))6$))7$))8$)))86$))7$))8$))))600$))1$))2$))3$))4$))5$))6$))7$))8$)))10$))1$))2$))3$))4$))5$))6$))7$))8$)))20$))1$))2$))3$))4$))5$))6$))7$))8$)))30$))1$))2$))3$))4$))5$))6$))7$))8$)))40$))1$))2$))3$))4$))5$))6$)))50$))1$)))60$))1$))3$))))700$))1$))2$))3$))4$))6$))))))))))))))']
        r = requests.get('http://127.0.0.1:8000/boundaries/', params=params)
        assert r.status_code == 200

        num_boundaries = 0
        for boundary in r.json():
            assert boundaries.__contains__(boundary['boundary'])
            num_boundaries = num_boundaries + 1
        assert num_boundaries == len(boundaries)

        store.dropAll()

        print('TEST FINISH')


if __name__ == "__main__":
    shp = TestsEmocionesBoundaries(
        "/Users/javiermartinez/Documents/UNIVERSIDAD/TFG/Datos_emociones_boundaries/MALLA_INTER/")
    shp.test_API()
    shp.test_API_polygon_P03()
    shp.test_API_polygon_P21()
    shp.test_API_polygon_P11()
    shp.test_API_polygon_P26()

