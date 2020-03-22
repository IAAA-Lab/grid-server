
class BoundaryDataSet:

    def __init__(self, boundary_data_set=None):
        """
        :param boundary_data_set: dictionary with optimal boundary identifier as key
        and OptimalBoundary and associated Data pairs as value:
        {
            BoundaryID.value: (OptimalBoundary,Data)
        }
        """
        if boundary_data_set is None:
            boundary_data_set = {}
        self.boundary_data_set = boundary_data_set

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
