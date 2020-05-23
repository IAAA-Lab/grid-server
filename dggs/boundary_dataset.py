import json

from dggs.boundary import Boundary, OptimalBoundary
from dggs.boundary_ID import BoundaryID, AUID
from dggs.data import Data
from dggs.rHealPix import rHEALPix


class BoundaryDataSet:

    def __init__(self, id,  boundary_data_set=None, dggs=rHEALPix(N_side=3, north_square=0, south_square=0)):
        """
        :param id: boundary dataset identifier
        :param boundary_data_set: dictionary with optimal boundary identifier as key
        and OptimalBoundary and associated Data pairs as value:
        {
            BoundaryID.value: (OptimalBoundary,Data)
        }
        :param dggs: Discrete Global Grid System, rHEALPix by default
        """
        assert id is not None
        self.id = id

        if boundary_data_set is None:
            boundary_data_set = {}
        self.boundary_data_set = boundary_data_set
        self.dggs = dggs

    def add(self, boundary, data):
        """
        Add a pair (Boundary, Data)
        :param boundary: object of type Boundary or OptimalBoundary.
        If it is not optimal, it is optimized before saving it in the dictionary.
        :param data: object of type Data.
        """
        if boundary.is_optimal():
            self.boundary_data_set[boundary.boundary_ID.value] = (boundary, data)
        else:
            optimal_boundary = boundary.optimize()
            self.boundary_data_set[optimal_boundary.boundary_ID.value] = (optimal_boundary, data)

    def add_list(self, boundary_data_list):
        """
        Add all pairs (Boundary, Data) in a list
        :param boundary_data_list: list of boundaries and associated data tuples
        If it is not optimal, it is optimized before saving it in the dictionary.
        """
        for (boundary, data) in boundary_data_list:
            if boundary.is_optimal():
                self.boundary_data_set[boundary.boundary_ID.value] = (boundary, data)
            else:
                optimal_boundary = boundary.optimize()
                self.boundary_data_set[optimal_boundary.boundary_ID.value] = (optimal_boundary, data)

    def get_boundaries(self):
        """
        :return: list with all the boundaries of the set
        """
        boundary_list = []
        for boundary_ID, (boundary, data) in self.boundary_data_set.items():
            boundary_list.append(boundary)
        return boundary_list

    def get_boundaries_and_data(self):
        """
        :return: list of tuples (Boundary, Data) with all the boundaries and data of the set
        """
        boundary_data_list = []
        for boundary_ID, value in self.boundary_data_set.items():
            boundary_data_list.append(value)
        return boundary_data_list

    def get_min_refinement(self):
        """
        :return: integer that represents the minimum refinement of the set
        """
        (boundary, data) = list(self.boundary_data_set.values())[0]
        min_refinement = boundary.get_min_refinement()
        for boundary_ID, (boundary, data) in self.boundary_data_set.items():
            if boundary.get_min_refinement() < min_refinement:
                min_refinement = boundary.get_min_refinement()
        return min_refinement

    def get_max_refinement(self):
        """
        :return: integer that represents the maximum refinement of the set
        """
        (boundary, data) = list(self.boundary_data_set.values())[0]
        max_refinement = boundary.get_max_refinement()
        for boundary_ID, (boundary, data) in self.boundary_data_set.items():
            if boundary.get_min_refinement() > max_refinement:
                max_refinement = boundary.get_max_refinement()
        return max_refinement

    def get_boundary_data(self, boundary_ID):
        """
        :param boundary_ID: boundary identifier, of type BoundaryID
        :return: data associated with the boundary with identifier boundary_ID
        """
        return self.boundary_data_set[boundary_ID.value][1]

    def get_boundary_data_list(self, boundary_ID_list):
        """
        :param boundary_ID_list: list of boundary identifiers, of type BoundaryID
        :return: list of data associated with the boundaries with identifier boundary_ID
        """
        data_list = []
        for boundary_ID in boundary_ID_list:
            data_list.append(self.boundary_data_set[boundary_ID.value][1])
        return data_list

    def print(self):
        """
        Prints the pairs of boundary identifiers with their associated data from the set.
        """
        for boundary_ID, (boundary, data) in self.boundary_data_set.items():
            print(boundary_ID, data.content)

    def toJSON(self, optimal):
        boundary_list = []
        for AUID, (boundary, data) in self.boundary_data_set.items():
            if optimal:
                dic = {
                    'AUID': AUID,
                    'boundary': boundary.AUID_to_ID(),
                    'data': data.content
                }
            else:
                dic = {
                    'boundary': boundary.AUID_to_ID(),
                    'data': data.content
                }
            boundary_list.append(dic)

        bds = {
            'id': self.id,
            'boundary_data_set': boundary_list,
        }
        return json.dumps(bds)

    def fromJSON(self, bds_json):
        bds = json.loads(bds_json)
        self.boundary_data_set = {}
        self.id = bds['id']
        boundary_list = bds['boundary_data_set']

        for boundary in boundary_list:
            self.add(OptimalBoundary(boundary_ID=AUID(boundary['AUID'])), Data(boundary['data']))

        return self
