import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_dataset import BoundaryDataSet
from dggs.cell_ID import CellID
from dggs.cell_dataset import CellDataSet
from dggs.data import Data

"""
BOUNDARY_DATASET_IDs
"""

class BoundaryDatasetIDSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=400)

"""
CELL_DATASET_IDs
"""

class CellDatasetIDSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=400)

"""
BOUNDARY_DATASET
"""

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
    id = serializers.CharField(max_length=400)
    boundary_data_set = BoundaryDatasetField()

    def save(self, store):
        bds = BoundaryDataSet(id=self.validated_data['id'], boundary_data_set=self.validated_data['boundary_data_set'])
        store.insert(bds)


class BoundaryDatasetUpdateSerializer(serializers.Serializer):
    boundary_data_set = BoundaryDatasetField()

    def save(self, store, bds_id):
        bds = BoundaryDataSet(id=bds_id, boundary_data_set=self.validated_data['boundary_data_set'])
        store.update_boundary_dataset(bds)


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


class DataField(serializers.Field):
    def to_representation(self, data):
        return data

    def to_internal_value(self, data):
        return data


class BoundaryDataUpdateSerializer(serializers.Serializer):
    data = DataField()

    def save(self, store, bds_id, boundary_id):
        store.update_boundary_in_boundary_datasets(bds_id, Boundary(boundary_ID=BoundaryID(boundary_id)).optimize(),
                                                   Data(self.validated_data['data']))


"""
CELL_DATASET
"""

class CellDatasetField(serializers.Field):
    def to_representation(self, cell_data_set):
        cds_representation = []
        for id, (cell_id, data) in cell_data_set.items():
            dic = {
                'cellID': id,
                'data': data.content
            }
            cds_representation.append(dic)
        return cds_representation

    def to_internal_value(self, data):
        cds = CellDataSet(id='')
        for item in data:
            if not re.match(r'^[A-Za-z0-9]+$', item['cellID']):
                raise ValidationError('Incorrect format: ' + item['cellID'])
            cds.add(CellID(item['cellID']), Data(item['data']))
        return cds.cell_data_set


class CellDatasetSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    cell_data_set = CellDatasetField()

    def save(self, store):
        cds = CellDataSet(id=self.validated_data['id'], cell_data_set=self.validated_data['cell_data_set'])
        store.insert(cds)


class CellDatasetUpdateSerializer(serializers.Serializer):
    cell_data_set = CellDatasetField()

    def save(self, store, cds_id):
        cds = CellDataSet(id=cds_id, cell_data_set=self.validated_data['cell_data_set'])
        store.update_cell_dataset(cds)


class CellDataSerializer(serializers.Serializer):
    cellID = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_cellID(self, obj):
        return obj[0].value

    def get_data(self, obj):
        return obj[1].content


class CellDataUpdateSerializer(serializers.Serializer):
    data = DataField()

    def save(self, store, cds_id, cellID):
        store.update_cell_in_cell_datasets(cds_id, CellID(cellID), Data(self.validated_data['data']))
