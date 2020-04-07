from pymongo import MongoClient
from rest_framework import viewsets, status
from rest_framework.response import Response
from api_dggs.api.serializer import BoundaryDatasetSerializer, BoundaryDataSerializer
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_store import BoundaryStore
import re


class BoundaryDatasetsView(viewsets.ViewSet):
    serializer_class = BoundaryDatasetSerializer
    store = BoundaryStore(MongoClient(port=27017).bds)

    def list(self, request):
        try:
            boundaries_datasets = self.store.all_boundary_datasets()
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=boundaries_datasets, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(store=self.store)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            boundaries_datasets = self.store.query_by_boundary_to_boundary_datasets(
                Boundary(boundary_ID=BoundaryID(pk)))
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.serializer_class(
            instance=boundaries_datasets, many=True)
        return Response(serializer.data)


class BoundaryView(viewsets.ViewSet):
    serializer_class = BoundaryDataSerializer
    store = BoundaryStore(MongoClient(port=27017).bds)

    def list(self, request):
        dlx = self.request.query_params.get('dlx', None)
        dly = self.request.query_params.get('dly', None)
        drx = self.request.query_params.get('drx', None)
        dry = self.request.query_params.get('dry', None)
        urx = self.request.query_params.get('urx', None)
        ury = self.request.query_params.get('ury', None)
        ulx = self.request.query_params.get('ulx', None)
        uly = self.request.query_params.get('uly', None)

        if (dlx and dly and drx and dry and urx and ury and ulx and uly) is not None:
            polygon = [[[float(dlx), float(dly)], [float(drx), float(dry)],
                        [float(urx), float(ury)], [float(ulx), float(uly)], [float(dlx), float(dly)]]]
            try:
                boundaries = self.store.query_by_polygon(polygon)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=boundaries, many=True)
        elif ((dlx and dly and urx and ury) is not None) and ((drx and dry and ulx and uly) is None):
            polygon = [[[float(dlx), float(dly)], [float(urx), float(dly)],
                        [float(urx), float(ury)], [float(dlx), float(ury)], [float(dlx), float(dly)]]]
            print(polygon)
            try:
                boundaries = self.store.query_by_polygon(polygon)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=boundaries, many=True)
        else:
            try:
                boundaries_datasets = self.store.all_boundaries()
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=boundaries_datasets, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if not re.match(r'^[A-Za-z0-9]+$', pk):
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            boundaries = self.store.query_by_boundary(Boundary(boundary_ID=BoundaryID(pk)))
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=boundaries, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        print('Destroy')

        if not re.match(r'^[A-Za-z0-9]+$', pk):
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.store.delete(Boundary(boundary_ID=BoundaryID(pk)))
            print()
            if result == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
