from rest_framework import viewsets

from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import permissions
from manager.models import Manager

from .models import Vehicle, Brand, Driver, Enterprise, DriverVehicleAssignment
from .serializers import (
    VehicleSerializer,
    BrandSerializer,
    DriverSerializer,
    EnterpriseSerializer,
    DriverVehicleAssignmentSerializer
)

@method_decorator(csrf_protect, name='dispatch')
class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'manager'):
            return Enterprise.objects.filter(managers=user.manager)
        return Enterprise.objects.none()

@method_decorator(csrf_protect, name='dispatch')
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

@method_decorator(csrf_protect, name='dispatch')
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.select_related('brand', 'company', 'active_driver')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'manager'):
            # Получаем предприятия, которыми управляет менеджер
            enterprises = user.manager.enterprises.all()
            return Vehicle.objects.filter(company__in=enterprises)
        return Vehicle.objects.none()

@method_decorator(csrf_protect, name='dispatch')
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.select_related('company')
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'manager'):
            # Получаем предприятия, которыми управляет менеджер
            enterprises = user.manager.enterprises.all()
            return Driver.objects.filter(company__in=enterprises)
        return Driver.objects.none()

@method_decorator(csrf_protect, name='dispatch')
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