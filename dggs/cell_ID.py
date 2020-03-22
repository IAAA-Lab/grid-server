class CellID:
    def __init__(self, value):
        """
        :param value: string representing the cell identifier
        """
        self.value = value

    def __eq__(self, other):
        return (other is not None) and (self.value == other.value)

    def get_refinement(self):
        """
        :return: integer that represents the refinement (resolution) of the cell
        """
        return len(self.value) - 1
