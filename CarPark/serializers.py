from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Vehicle, Brand
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ('brand_id',)
#
# class VehicleSerializer(serializers.HyperlinkedModelSerializer):
#     brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
#     class Meta:
#         model = Vehicle
#         fields = ('car_id', 'car_number', 'car_cost', 'car_year', 'car_mileage', 'car_color', 'brand')
#
from rest_framework import serializers
from .models import Vehicle, Brand, Driver, Enterprise, DriverVehicleAssignment


class EnterpriseSerializer(serializers.HyperlinkedModelSerializer):
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Enterprise
        fields = ('e_id', 'e_name', 'e_city', 'e_address', 'vehicles')

    def get_vehicles(self, obj):
        return [
            {
                'car_id': vehicle.car_id,
                'assigned_drivers': list(vehicle.drivers.values_list('d_id', flat=True))
            }
            for vehicle in obj.vehicle_set.all()
        ]


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    active_vehicle_id = serializers.SerializerMethodField()
    assigned_vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ('d_id', 'd_name', 'd_salary', 'd_license', 'active_vehicle_id', 'assigned_vehicles')

    def get_active_vehicle_id(self, obj):
        # Получаем активное назначение (если есть)
        active_assignment = DriverVehicleAssignment.objects.filter(
            driver=obj,
            is_active=True
        ).first()
        return active_assignment.vehicle.car_id if active_assignment else None

    def get_assigned_vehicles(self, obj):
        # Получаем все назначенные автомобили (только ID)
        return list(
            obj.drivervehicleassignment_set.all().values_list('vehicle__car_id', flat=True)
        )


class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    active_driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), allow_null=True)

    class Meta:
        model = Vehicle
        fields = ('car_id', 'car_number', 'car_cost', 'car_year', 'car_mileage',
                  'car_color', 'brand', 'active_driver')


class DriverVehicleAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DriverVehicleAssignment
        fields = ('id', 'driver', 'vehicle', 'assignment_date', 'is_active')

# User = get_user_model()
#
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email', ''),
#             password=validated_data['password']
#         )
#         return user
#
# class CustomTokenObtainSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Добавление кастомных полей в токен (опционально)
#         token['username'] = user.username
#         return token