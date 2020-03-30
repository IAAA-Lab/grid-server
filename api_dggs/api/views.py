from pymongo import MongoClient
from rest_framework import viewsets, status
from rest_framework.response import Response
from api_dggs.api.serializer import BoundaryDatasetSerializer
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_store import BoundaryStore

class BoundaryDatasetsView(viewsets.ViewSet):
    serializer_class = BoundaryDatasetSerializer
    store = BoundaryStore(MongoClient(port=27017).bds)

    def list(self, request):
        boundaries_datasets = self.store.all_boundary_datasets()
        serializer = self.serializer_class(
            instance=boundaries_datasets, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(store=self.store)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        boundaries_datasets = self.store.query_by_boundary_to_boundary_datasets(Boundary(boundary_ID=BoundaryID(pk)))
        serializer = self.serializer_class(
            instance=boundaries_datasets, many=True)
        return Response(serializer.data)
