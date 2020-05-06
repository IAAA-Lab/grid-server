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
        for AUID, (boundary, data) in boundary_data_set.items():
            dic = {
                'AUID': AUID,
                'boundary': boundary.AUID_to_ID(),
                'data': data.content
            }
            bds_representation.append(dic)
        return bds_representation

    def to_internal_value(self, data):
        bds = BoundaryDataSet(id='')
        for item in data:
            if not re.match(r'^[A-Za-z0-9]+$', item['boundary']):
                raise ValidationError('Incorrect format: ' + item['boundary'])
            bds.add(Boundary(boundary_ID=BoundaryID(item['boundary'])), Data(item['data']))
        return bds.boundary_data_set


class BoundaryDatasetSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    boundary_data_set = BoundaryDatasetField()

    def save(self, store):
        bds = BoundaryDataSet(id=self.validated_data['id'], boundary_data_set=self.validated_data['boundary_data_set'])
        store.insert(bds)


class BoundaryDataSerializer(serializers.Serializer):
    AUID = serializers.SerializerMethodField()
    boundary = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_AUID(self, obj):
        return obj[0].boundary_ID.value

    def get_boundary(self, obj):
        return obj[0].AUID_to_ID()

    def get_data(self, obj):
        return obj[1].content
