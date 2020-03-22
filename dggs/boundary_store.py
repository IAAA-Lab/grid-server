import pymongo
from bson import ObjectId
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
        Insert, in the collection of boundaries, one _boundary for each pair in the set, derived from its auid,
        bounding box and associated data. Insert, in the collection of boundaries datasets,
        a _boundaryDataSet formed by the list of inserted boundaries.

        :param b_dataset: BoundaryDataSet containing the OptimalBoundary and Data pairs.
        """
        boundary_data_set = b_dataset.boundary_data_set
        boundaries = []
        for boundary_ID, (boundary, data) in boundary_data_set.items():
            _boundary = {
                "oID": ObjectId(),  # TODO
                "auid": boundary_ID,
                "bbox": {
                    "type": "Polygon",
                    "coordinates": boundary.get_bbox(),
                },
                "data": data.content
            }
            self.db.boundaries.insert_one(_boundary)
            boundaries.append(_boundary["oID"])

        _boundaryDataSet = {
            "oID": ObjectId(),
            "boundaries": boundaries
        }
        self.db.b_data_sets.insert_one(_boundaryDataSet)
        self.db.boundaries.create_index([("bbox", pymongo.GEOSPHERE)])

    def query__by_boundary(self, boundary):
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

    def query__by_polygon(self, polygon):
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

    def delete(self, boundary):
        """
        :param boundary: Boundary or OptimalBoundary. If it is not optimal, it is optimized before making the query.
        :return: Delete stored boundaries that have the same identifier as the param
        """
        if boundary.is_optimal():
            optimal_boundary = boundary
        else:
            optimal_boundary = boundary.optimize()

        boundaries = self.db.boundaries.find({"auid": optimal_boundary.boundary_ID.value})
        for boundaryFounded in boundaries:
            b_data_sets = self.db.b_data_sets.find({"boundaries": boundaryFounded["oID"]})

            for b_data_set in b_data_sets:
                new_boundaries = [objectID for objectID in b_data_set["boundaries"] if
                                  objectID != boundaryFounded["oID"]]
                self.db.b_data_sets.update_many(
                    {"oID": b_data_set["oID"]},
                    {
                        "$set": {"boundaries": new_boundaries},
                    }
                )
            self.db.boundaries.delete_many({"oID": boundaryFounded["oID"]})

    def dropAll(self):
        """
        Delete stored data
        """
        self.db.boundaries.drop()
        self.db.b_data_sets.drop()
