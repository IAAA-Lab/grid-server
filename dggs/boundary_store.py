import pymongo
from bson import ObjectId

from dggs.boundary import OptimalBoundary
from dggs.boundary_ID import AUID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class BoundaryStore:

    def __init__(self, bds, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param bds: database
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.dggs = dggs
        self.db = bds

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
        boundary_dataset_id = ObjectId()
        _boundaryDataSet = {
            "_id": boundary_dataset_id,
        }
        self.db.b_data_sets.insert_one(_boundaryDataSet)

        # Store boundaries
        for (boundary, data) in b_dataset.get_all():
            _boundary = {
                "auid": boundary.boundary_ID.value,
                "bbox": {
                    "type": "Polygon",
                    "coordinates": boundary.get_bbox(),
                },
                "data": data.content,
                "boundary_dataset_id": boundary_dataset_id
            }
            self.db.boundaries.insert_one(_boundary)
        self.db.boundaries.create_index([("bbox", pymongo.GEOSPHERE)])

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

    def all_boundary_datasets(self):
        """
        :return: List of all stored BoudnariesDatasets
        """
        boundary_data_sets = []
        boundaries_datasets_founded = self.db.b_data_sets.find()
        for boundary_dataset in boundaries_datasets_founded:
            bds = BoundaryDataSet()
            boundaries_in_bds_founded = self.db.boundaries.find({"boundary_dataset_id": boundary_dataset["_id"]})
            for boundary in boundaries_in_bds_founded:
                bds.add(OptimalBoundary(boundary_ID=AUID(boundary["auid"])), Data(boundary["data"]))
            boundary_data_sets.append(bds)
        return boundary_data_sets

    def delete(self, boundary):
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

    def dropAll(self):
        """
        Delete stored data
        """
        self.db.boundaries.drop()
        self.db.b_data_sets.drop()