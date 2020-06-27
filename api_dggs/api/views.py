import re
from rest_framework import viewsets, status
from rest_framework.response import Response

from api_dggs.api.serializer import BoundaryDatasetSerializer, BoundaryDataSerializer,\
    BoundaryDatasetUpdateSerializer, BoundaryDataUpdateSerializer, CellDatasetSerializer, CellDatasetUpdateSerializer, \
    CellDataUpdateSerializer, CellDataSerializer, BoundaryDatasetIDSerializer, CellDatasetIDSerializer
from dggs.boundary import Boundary
from dggs.boundary_ID import BoundaryID
from dggs.boundary_store import BoundaryStore
from dggs.cell_ID import CellID
from dggs.cell_store import CellStore


"""
BOUNDARY_DATASET_IDs
"""

class BoundaryDatasetsIDsView(viewsets.ViewSet):
    serializer_class = BoundaryDatasetIDSerializer
    store = BoundaryStore()

    def list(self, request):
        try:
            boundaries_datasets_ids = self.store.boundary_datasets_ids()
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=boundaries_datasets_ids, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk == 'last':
            try:
                boundary_datasets_last_id = self.store.boundary_datasets_last_id()
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=boundary_datasets_last_id)
            return Response(serializer.data)

"""
CELL_DATASET_IDs
"""

class CellDatasetsIDsView(viewsets.ViewSet):
    serializer_class = CellDatasetIDSerializer
    store = CellStore()

    def list(self, request):
        try:
            cell_datasets_ids = self.store.cell_datasets_ids()
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=cell_datasets_ids, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if pk == 'last':
            try:
                bcell_datasets_last_id = self.store.cell_datasets_last_id()
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=bcell_datasets_last_id)
            return Response(serializer.data)


"""
BOUNDARY_DATASET
"""

class BoundaryDatasetsView(viewsets.ViewSet):
    serializer_class = BoundaryDatasetSerializer
    update_bds_serializer_class = BoundaryDatasetUpdateSerializer
    update_boundary_serializer_class = BoundaryDataUpdateSerializer
    store = BoundaryStore()

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

    def retrieve(self, request, bds=None, pk=None):
        if bds is not None:
            if not re.match(r'^[A-Za-z0-9]+$', pk):
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                boundary_dataset = self.store.query_by_boundary_in_boundary_datasets(bds, Boundary(
                    boundary_ID=BoundaryID(pk)))
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.serializer_class(
                instance=boundary_dataset, many=True)
        else:
            try:
                boundary_dataset = self.store.all_boundaries_in_dataset(pk)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.serializer_class(
                instance=boundary_dataset, many=True)
        return Response(serializer.data)

    def update(self, request, bds=None, pk=None):
            if bds is not None:
                print(request.data)
                serializer = self.update_boundary_serializer_class(data=request.data)
                if serializer.is_valid():
                    try:
                        result = serializer.save(store=self.store, bds_id=bds, boundary_id=pk)
                        if result == 0:
                            return Response(status=status.HTTP_404_NOT_FOUND)
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
            else:
                serializer = self.update_bds_serializer_class(data=request.data)
                if serializer.is_valid():
                    try:
                        serializer.save(store=self.store, bds_id=pk)
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



    def destroy(self, request, bds=None, pk=None):
        if bds is not None:
            if not re.match(r'^[A-Za-z0-9]+$', pk):
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                result = self.store.delete_boundary_in_boundary_datasets(bds, Boundary(boundary_ID=BoundaryID(pk)))
                if result == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                result = self.store.delete_boundary_dataset(pk)
                if result == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BoundaryView(viewsets.ViewSet):
    serializer_class = BoundaryDataSerializer
    store = BoundaryStore()

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

    def retrieve(self, request, pk=None, boundary=None):
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

        if not re.match(r'^[A-Za-z0-9]+$', pk):
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.store.delete_boundary(Boundary(boundary_ID=BoundaryID(pk)))
            if result == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
CELL_DATASET
"""

class CellDatasetsView(viewsets.ViewSet):
    serializer_class = CellDatasetSerializer
    update_cds_serializer_class = CellDatasetUpdateSerializer
    update_cell_serializer_class = CellDataUpdateSerializer
    store = CellStore()

    def list(self, request):
        try:
            cell_datasets = self.store.all_cell_datasets()
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=cell_datasets, many=True)
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

    def retrieve(self, request, cds=None, pk=None):
        if cds is not None:
            if not re.match(r'^[A-Za-z0-9]+$', pk):
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                cell_dataset = self.store.query_by_cell_in_cell_datasets(cds, CellID(pk))
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.serializer_class(
                instance=cell_dataset, many=True)
        else:
            try:
                cell_dataset = self.store.all_cells_in_dataset(pk)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.serializer_class(
                instance=cell_dataset, many=True)
        return Response(serializer.data)

    def update(self, request, cds=None, pk=None):
            if cds is not None:
                print(request.data)
                serializer = self.update_cell_serializer_class(data=request.data)
                if serializer.is_valid():
                    try:
                        result = serializer.save(store=self.store, cds_id=cds, cellID=pk)
                        if result == 0:
                            return Response(status=status.HTTP_404_NOT_FOUND)
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
            else:
                serializer = self.update_cds_serializer_class(data=request.data)
                if serializer.is_valid():
                    try:
                        serializer.save(store=self.store, cds_id=pk)
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

    def destroy(self, request, cds=None, pk=None):
        if cds is not None:
            if not re.match(r'^[A-Za-z0-9]+$', pk):
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                result = self.store.delete_cell_in_cell_datasets(cds, CellID(pk))
                if result == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                result = self.store.delete_cell_dataset(pk)
                if result == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CellView(viewsets.ViewSet):
    serializer_class = CellDataSerializer
    store = CellStore()

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
                cells = self.store.query_by_polygon(polygon)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=cells, many=True)
        elif ((dlx and dly and urx and ury) is not None) and ((drx and dry and ulx and uly) is None):
            polygon = [[[float(dlx), float(dly)], [float(urx), float(dly)],
                        [float(urx), float(ury)], [float(dlx), float(ury)], [float(dlx), float(dly)]]]
            print(polygon)
            try:
                cells = self.store.query_by_polygon(polygon)
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=cells, many=True)
        else:
            try:

                cell_datasets = self.store.all_cells()
            except:
                return Response({
                    'status': 'Bad request',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = self.serializer_class(
                instance=cell_datasets, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, cell=None):
        if not re.match(r'^[A-Za-z0-9]+$', pk):
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cells = self.store.query_by_cell(CellID(pk))
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.serializer_class(
            instance=cells, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):

        if not re.match(r'^[A-Za-z0-9]+$', pk):
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = self.store.delete_cell(CellID(pk))
            if result == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'status': 'Bad request',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)