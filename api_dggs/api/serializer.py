import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.data import Data


class BoundaryDatasetField(serializers.Field):
    def to_representation(self, boundary_data_set):
        bds_representation = []
        for boundary_id, (boundary, data) in boundary_data_set.items():
            dic = {
                'boundary': boundary_id,
                'data': data.content
            }
            bds_representation.append(dic)
        return bds_representation

    def to_internal_value(self, data):
        bds = BoundaryDataSet()
        for item in data:
            if not re.match(r'^[A-Za-z0-9]+$', item['boundary']):
                raise ValidationError('Incorrect format.')

            bds.add(Boundary(boundary_ID=BoundaryID(item['boundary'])),  Data(item['data']))
        return bds.boundary_data_set


class BoundaryDatasetSerializer(serializers.Serializer):
    boundary_data_set = BoundaryDatasetField()

    def save(self, store):
        bds = BoundaryDataSet(self.validated_data['boundary_data_set'])
        store.insert(bds)

