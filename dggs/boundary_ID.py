class BoundaryID:
    def __init__(self, value):
        """
        :param value: string representing the boundary identifier
        """
        self.value = value
        self.hash = [] # TODO

    def getURL(self, baseURL):
        # TODO
        return


class AUID(BoundaryID):
    """
    :param value: string representing the boundary identifier as defined in the AGILE19 paper
    """
    pass
