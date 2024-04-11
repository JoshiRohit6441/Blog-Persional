from rest_framework import decorators, permissions as rest_permission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import CountryModel, CountryCode, StateModal, CityModal
from .serializer import CountryCodeSerialzier, CountryModelSerializer, CityModalSerializer, StateModalSerializer
from rest_framework.pagination import PageNumberPagination


class CustumPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'


class CountryCodeView(APIView):
    paginatuiion_class = CustumPagination

    @decorators.permission_classes([rest_permission.AllowAny])
    def get(self, request):
        country_code = CountryCode.objects.all()
        pagination = self.paginatuiion_class
        result = pagination.paginate_queryset(country_code, request)
        serializer = CountryCodeSerialzier(result, many=True)
        return Response({
            "message": "Country Code data",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def post(self, request):
        serializer = CountryCodeSerialzier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Country Code Created",
                "status": status.HTTP_201_CREATED,
            })
        else:
            return Response({
                "message": "Country Code Not Created",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def patch(self, request, id=None):
        country_code = CountryCode.objects.get(id=id)
        serializer = CountryCodeSerialzier(country_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Country Code Updated",
                "status": status.HTTP_200_OK,
            })
        else:
            return Response({
                "message": "Country Code Not Updated",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def delete(self, request, id=None):
        country_code = CountryCode.objects.get(id=id)
        country_code.delete()
        return Response({
            "message": "Country Code Deleted",
            "status": status.HTTP_200_OK,
        })


class CountryView(APIView):
    pagination_class = CustumPagination

    @decorators.permission_classes([rest_permission.AllowAny])
    def get(self, request):
        country = CountryModel.objects.all()
        pagination = self.pagination_class()
        result = pagination.paginate_queryset(country, request)
        serializer = CountryModelSerializer(result, many=True)
        return Response({
            "message": "Country data",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def post(self, request):
        serializer = CountryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Country Created",
                "status": status.HTTP_201_CREATED,
            })
        else:
            return Response({
                "message": "Country Not Created",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def patch(self, request, id=None):
        country = CountryModel.objects.get(id=id)
        serializer = CountryModelSerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Country Updated",
                "status": status.HTTP_200_OK,
            })
        else:
            return Response({
                "message": "Country Not Updated",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def delete(self, request, id=None):
        country = CountryModel.objects.get(id=id)
        country.delete()
        return Response({
            "message": "Country Deleted",
            "status": status.HTTP_200_OK,
        })


class StateView(APIView):
    pagination_class = CustumPagination

    @decorators.permission_classes([rest_permission.AllowAny])
    def get(self, request):
        state = StateModal.objects.all()
        pagination = self.pagination_class()
        result = pagination.paginate_queryset(state, request)
        serializer = StateModalSerializer(result, many=True)
        return Response({
            "message": "State data",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def post(self, request):
        serializer = StateModalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "State Created",
                "status": status.HTTP_201_CREATED,
            })
        else:
            return Response({
                "message": "State Not Created",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def patch(self, request, id=None):
        state = StateModal.objects.get(id=id)
        serializer = StateModalSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "State Updated",
                "status": status.HTTP_200_OK,
            })
        else:
            return Response({
                "message": "State Not Updated",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def delete(self, request, id=None):
        state = StateModal.objects.get(id=id)
        state.delete()
        return Response({
            "message": "State Deleted",
            "status": status.HTTP_200_OK,
        })


class CityView(APIView):
    pagination_class = CustumPagination

    @decorators.permission_classes([rest_permission.AllowAny])
    def get(self, request):
        city = CityModal.objects.all()
        pagination = self.pagination_class
        result = pagination.paginate_queryset(city, request)
        serializer = CityModalSerializer(result, many=True)
        return Response({
            "message": "City data",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def post(self, request):
        serializer = CityModalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "City Created",
                "status": status.HTTP_201_CREATED,
            })
        else:
            return Response({
                "message": "City Not Created",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def patch(self, request, id=None):
        city = CityModal.objects.get(id=id)
        serializer = CityModalSerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "City Updated",
                "status": status.HTTP_200_OK,
            })
        else:
            return Response({
                "message": "City Not Updated",
                "status": status.HTTP_400_BAD_REQUEST,
            })

    @decorators.permission_classes([rest_permission.IsAdminUser])
    def delete(self, request, id=None):
        city = CityModal.objects.get(id=id)
        city.delete()
        return Response({
            "message": "City Deleted",
            "status": status.HTTP_200_OK,
        })
