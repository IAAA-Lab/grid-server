import pymongo
from pymongo import MongoClient

from dggs.boundary import OptimalBoundary
from dggs.boundary_ID import AUID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.data import Data
from dggs.rHealPix import rHEALPix
import mongodb_config
from bson import ObjectId

class BoundaryStore:

    def __init__(self, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.dggs = dggs
        self.db = MongoClient(mongodb_config.MONGODB_CONFIG['host']).bds

    def get_Boundary_Data(self, boundary):
        """
        :param boundary: document stored that contains the boundary_id and data associated
        :return: OptimalBoundary and Data tuple
        """
        return OptimalBoundary(boundary_ID=AUID(boundary["auid"])), Data(boundary["data"])

    def insert(self, b_dataset):
        """
        Insert, in the collection of boundaries datasets, a _boundaryDataSet formed by its identifier.

        Insert, in the collection of boundaries, one _boundary for each pair in the set, derived from its auid,
        bounding box, associated data and the identifier of the _boundaryDataSet.

        :param b_dataset: BoundaryDataSet containing the OptimalBoundary and Data pairs.
        """

        # Store boundaryDataSet
        _boundaryDataSet = {
            "_id": b_dataset.id,
            "insertID": ObjectId(),
        }
        self.db.b_data_sets.insert_one(_boundaryDataSet)

        # Store boundaries
        for (boundary, data) in b_dataset.get_boundaries_and_data():
            _boundary = {
                "auid": boundary.boundary_ID.value,
                "bbox": {
                    "type": "Polygon",
                    "coordinates": boundary.get_bbox(),
                },
                "data": data.content,
                "boundary_dataset_id": b_dataset.id
            }
            self.db.boundaries.insert_one(_boundary)
        self.db.boundaries.create_index([("bbox", pymongo.GEOSPHERE)])

    """
    BOUNDARIES
    """
    def all_boundaries(self):
        """
        :return: List of all stored Boundaries and Data associated
        """
        boundaries_founded = self.db.boundaries.find()
        boundaries = []
        for boundary in boundaries_founded:
            boundary, data = self.get_Boundary_Data(boundary)
            boundaries.append((boundary, data))
        return boundaries

    def query_by_boundary(self, boundary):
        """
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: List of tuples with stored boundaries that have the same identifier as the param and data associated
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries_founded = self.db.boundaries.find({"auid": optimal_boundary.boundary_ID.value})
        boundaries = []
        for boundary in boundaries_founded:
            boundary, data = self.get_Boundary_Data(boundary)
            boundaries.append((boundary, data))
        return boundaries

    def query_by_polygon(self, polygon):
        """
        :param polygon: Polygon with which you want to make the intersection
        :return: List of tuples with stored boundaries that intersect the polygon and data associated
        """
        boundaries_founded = self.db.boundaries.find(
            {
                "bbox": {
                    "$geoIntersects": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": polygon,
                            "crs": {
                                "type": "name",
                                "properties": {"name": "urn:x-mongodb:crs:strictwinding:EPSG:4326"}
                            }
                        }
                    }
                }
            }
        )
        boundaries = []
        for boundary in boundaries_founded:
            boundary, data = self.get_Boundary_Data(boundary)
            boundaries.append((boundary, data))
        return boundaries

    def delete_boundary(self, boundary):
        """
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: Delete stored boundaries that have the same identifier as the param
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        result = self.db.boundaries.delete_many({"auid": optimal_boundary.boundary_ID.value})

        return result.deleted_count

    """
    BOUNDARY_DATASETS
    """
    def all_boundary_datasets(self):
        """
        :return: List of all stored BoundaryDatasets
        """
        boundary_data_sets = []
        boundaries_datasets_founded = self.db.b_data_sets.find()
        for boundary_dataset in boundaries_datasets_founded:
            bds = BoundaryDataSet(id=boundary_dataset["_id"])
            boundaries_in_bds_founded = self.db.boundaries.find({"boundary_dataset_id": boundary_dataset["_id"]})
            for boundary in boundaries_in_bds_founded:
                bds.add(OptimalBoundary(boundary_ID=AUID(boundary["auid"])), Data(boundary["data"]))
            boundary_data_sets.append(bds)
        return boundary_data_sets

    def query_by_boundary_to_boundary_datasets(self, boundary):
        """
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: List of BoundaryDataSets where boundary is located
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries_founded = self.db.boundaries.find({"auid": optimal_boundary.boundary_ID.value})

        boundary_data_sets = []
        for boundary in boundaries_founded:
            bds = BoundaryDataSet()
            boundaries_in_bds_founded = self.db.boundaries.find(
                {"boundary_dataset_id": boundary["boundary_dataset_id"]})
            for boundary_2 in boundaries_in_bds_founded:
                boundary, data = self.get_Boundary_Data(boundary_2)
                bds.add(boundary, data)
            boundary_data_sets.append(bds)
        return boundary_data_sets

    def all_boundaries_in_dataset(self, id):
        """
        :param id: identifier of the BoundaryDataset
        :return: List of tuples with stored boundaries and data associated stored in the BoundaryDataset with that id.
        """
        boundaries_datasets_founded = self.db.b_data_sets.find({"_id": id})
        boundary_data_sets = []
        for boundary_dataset in boundaries_datasets_founded:
            bds = BoundaryDataSet(id=id)
            boundaries_in_bds_founded = self.db.boundaries.find({"boundary_dataset_id": boundary_dataset["_id"]})
            for boundary in boundaries_in_bds_founded:
                bds.add(OptimalBoundary(boundary_ID=AUID(boundary["auid"])), Data(boundary["data"]))
            boundary_data_sets.append(bds)
        return boundary_data_sets

    def query_by_boundary_in_boundary_datasets(self, id, boundary):
        """
        :param id: identifier of the BoundaryDataset
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: Boundary and data associated stored in the BoundaryDataset with that id.
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries_datasets_founded = self.db.b_data_sets.find({"_id": id})
        boundary_data_sets = []
        for boundary_dataset in boundaries_datasets_founded:
            bds = BoundaryDataSet(id=id)
            boundaries_in_bds_founded = self.db.boundaries.find({"boundary_dataset_id": boundary_dataset["_id"],
                                                                "auid": optimal_boundary.boundary_ID.value})
            for boundary in boundaries_in_bds_founded:
                bds.add(OptimalBoundary(boundary_ID=AUID(boundary["auid"])), Data(boundary["data"]))
            boundary_data_sets.append(bds)
        return boundary_data_sets

    def update_boundary_dataset(self, bds):
        """
        :param bds:
        :return: Update the BoundaryDataset with that id.
        """
        boundaries_datasets_founded = self.db.b_data_sets.find({"_id": bds.id})
        for boundary_dataset in boundaries_datasets_founded:
            self.db.boundaries.delete_many({"boundary_dataset_id": bds.id})
            for (boundary, data) in bds.get_boundaries_and_data():
                _boundary = {
                    "auid": boundary.boundary_ID.value,
                    "bbox": {
                        "type": "Polygon",
                        "coordinates": boundary.get_bbox(),
                    },
                    "data": data.content,
                    "boundary_dataset_id": boundary_dataset["_id"]
                }
                self.db.boundaries.insert_one(_boundary)
            self.db.boundaries.create_index([("bbox", pymongo.GEOSPHERE)])

    def update_boundary_in_boundary_datasets(self, bds_id, boundary, data):
        """
        :param bds_id: identifier of the BoundaryDataset
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: Update the stored boundary that have the same identifier as the param in the BoundaryDataset with that id.
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries_datasets_founded = self.db.b_data_sets.find({"_id": bds_id})
        for boundary_dataset in boundaries_datasets_founded:
            myquery = {"auid": optimal_boundary.boundary_ID.value, "boundary_dataset_id": boundary_dataset["_id"],}
            newvalues = {"$set": {"data": data.content}}

            return self.db.boundaries.update_many(myquery, newvalues)


    def delete_boundary_dataset(self, id):
        """
        :param id: identifier of the BoundaryDataset
        :return: Delete the BoundaryDataset with that id and all the boundaries and data  in it.
        """
        result1 = self.db.b_data_sets.delete_many({"_id": id})

        if result1.deleted_count > 0:
            self.db.boundaries.delete_many({"boundary_dataset_id": id})

        return result1.deleted_count

    def delete_boundary_in_boundary_datasets(self, id, boundary):
        """
        :param id: identifier of the BoundaryDataset
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: Delete the stored boundary that have the same identifier as the param in the BoundaryDataset with that id.
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        result = self.db.boundaries.delete_many({"boundary_dataset_id": id,
                                                                "auid": optimal_boundary.boundary_ID.value})

        return result.deleted_count

    def boundary_datasets_ids(self):
        """
        :return: List of all identifiers of stored datasets.
        """
        boundaries_datasets_founded = self.db.b_data_sets.find()
        id_list = []
        for bds in boundaries_datasets_founded:
            id_list.append({'id': bds['_id']})

        return id_list

    def boundary_datasets_last_id(self):
        """
        :return: Identifier of the last stored dataset.
        """
        boundaries_datasets_founded = self.db.b_data_sets.find().sort("insertID", -1).limit(1)
        last_id = ''
        for lastID in boundaries_datasets_founded:
            last_id = lastID['_id']

        return {'id': last_id}


    def dropAll(self):
        """
        Delete stored data
        """
        self.db.boundaries.drop()
        self.db.b_data_sets.drop()
