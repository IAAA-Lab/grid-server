import pymongo
from bson import ObjectId

from boundary import Boundary, OptimalBoundary
from boundary_ID import BoundaryID, AUID
from boundary_dataset import BoundaryDataSet
from data import Data
from rHealPix import rHEALPix


class BoundaryStore:

    def __init__(self, bds, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param bds: database
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        self.dggs = dggs
        self.db = bds

    def insert(self, b_dataset):
        """
        Insert, in the collection of boundaries datasets, a _boundaryDataSet formed by its identifier.

        Insert, in the collection of boundaries, one _boundary for each pair in the set, derived from its auid,
        bounding box, associated data and the identifier of the _boundaryDataSet.

        :param b_dataset: BoundaryDataSet containing the OptimalBoundary and Data pairs.
        """
        boundary_data_set = b_dataset.boundary_data_set

        # Store boundaryDataSet
        boundary_dataset_id = ObjectId()
        _boundaryDataSet = {
            "_id": boundary_dataset_id,
        }
        self.db.b_data_sets.insert_one(_boundaryDataSet)

        # Store boundaries
        for boundary_ID, (boundary, data) in boundary_data_set.items():
            _boundary = {
                "auid": boundary_ID,
                "bbox": {
                    "type": "Polygon",
                    "coordinates": boundary.get_bbox(),
                },
                "data": data.content,
                "boundary_dataset_id": boundary_dataset_id
            }
            self.db.boundaries.insert_one(_boundary)
        self.db.boundaries.create_index([("bbox", pymongo.GEOSPHERE)])

    def query_by_boundary(self, boundary):
        """
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: List of stored boundaries that have the same identifier as the param
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries_founded = self.db.boundaries.find({"auid": optimal_boundary.boundary_ID.value})

        return boundaries_founded

    def query_by_polygon(self, polygon):
        """
        :param polygon: Polygon with which you want to make the intersection
        :return: List of boundaries that intersect the polygon
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
        return boundaries_founded

    def query_boundary_datasets(self, boundary):
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
            boundaries_in_bds_founded = self.db.boundaries.find({"boundary_dataset_id": boundary["boundary_dataset_id"]})
            for boundary_2 in boundaries_in_bds_founded:
                bds.add(OptimalBoundary(boundary_ID=AUID(boundary_2["auid"])), Data(boundary_2["data"]["contentType"],
                                                                                  boundary_2["data"]["contentData"]))
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

        self.db.boundaries.delete_many({"auid": optimal_boundary.boundary_ID.value})


    def dropAll(self):
        """
        Delete stored data
        """
        self.db.boundaries.drop()
        self.db.b_data_sets.drop()
