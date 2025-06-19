from rest_framework import serializers
from CarPark.models import Enterprise
from .models import Manager
from CarPark.serializers import DriverSerializer, VehicleSerializer


class ManagerEnterpriseSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField()
    drivers = serializers.SerializerMethodField()

    class Meta:
        model = Enterprise
        fields = ('e_id', 'e_name', 'vehicles', 'drivers')

    def get_vehicles(self, obj):
        # Возвращаем только ID автомобилей
        return list(obj.vehicle_set.all().values_list('car_id', flat=True))

    def get_drivers(self, obj):
        # Возвращаем только ID водителей
        return list(obj.driver_set.all().values_list('d_id', flat=True))

class ManagerSerializer(serializers.ModelSerializer):
    enterprises = ManagerEnterpriseSerializer(many=True, read_only=True)

    class Meta:
        model = Manager
        fields = ('id', 'enterprises')

