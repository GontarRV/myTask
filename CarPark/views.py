# #from django.http import JsonResponse
# from rest_framework import viewsets
# from .serializers import BrandSerializer
# from .models import Brand
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import Vehicle
# from .serializers import VehicleSerializer
#
# class VehicleViewSet(viewsets.ModelViewSet):
#     queryset = Vehicle.objects.all().order_by('car_id')
#     serializer_class = VehicleSerializer
#
# class BrandViewSet(viewsets.ModelViewSet):
#     queryset = Brand.objects.all().order_by('brand_id')
#     serializer_class = BrandSerializer
#
# #class VehicleIndexAPI(APIView):
# #    def get(self, request):
# #        vehicles = Vehicle.objects.all()
# #        serializer = VehicleSerializer(vehicles, many=True)
# #        return JsonResponse(serializer.data, safe=False)

from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.response import Response
# from .serializers import UserRegistrationSerializer, CustomTokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Vehicle, Brand, Driver, Enterprise, DriverVehicleAssignment
from .serializers import (
    VehicleSerializer,
    BrandSerializer,
    DriverSerializer,
    EnterpriseSerializer,
    DriverVehicleAssignmentSerializer
)


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.select_related('brand', 'company', 'active_driver')
    serializer_class = VehicleSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        # Проверка при изменении предприятия
        if 'company' in serializer.validated_data and instance.drivers.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"company": "Нельзя изменить предприятие, пока есть назначенные водители"})
        serializer.save()


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('company')
    serializer_class = DriverSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        enterprise_id = self.request.query_params.get('enterprise')
        if enterprise_id:
            queryset = queryset.filter(company_id=enterprise_id)
        return queryset


class DriverVehicleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = DriverVehicleAssignment.objects.select_related('driver', 'vehicle')
    serializer_class = DriverVehicleAssignmentSerializer

    def perform_create(self, serializer):
        assignment = serializer.save()
        # Если назначение активно, обновляем активного водителя у автомобиля
        if assignment.is_active:
            assignment.vehicle.active_driver = assignment.driver
            assignment.vehicle.save()

    def perform_update(self, serializer):
        assignment = serializer.save()
        # Если назначение стало активным, обновляем активного водителя
        if assignment.is_active:
            assignment.vehicle.active_driver = assignment.driver
            assignment.vehicle.save()

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
# class LoginView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainSerializer