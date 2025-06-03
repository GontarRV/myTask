# from django.contrib import admin
# from .models import Vehicle, Brand
#
#
# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ("car_id", "car_number", "car_cost", "car_year",
#                     "car_mileage", "car_color", "brand")
#
# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("brand_id", "brand_name", "brand_tonnage", "brand_places",
#                     "brand_tank", "brand_door")

from django.contrib import admin
from .models import Vehicle, Brand, Driver, Enterprise, DriverVehicleAssignment


class DriverVehicleAssignmentInline(admin.TabularInline):
    model = DriverVehicleAssignment
    extra = 1
    raw_id_fields = ('driver', 'vehicle')


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('e_name', 'e_city', 'e_address')
    search_fields = ('e_name', 'e_city')
    list_filter = ('e_city',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'brand_tonnage', 'brand_places')
    search_fields = ('brand_name',)
    list_filter = ('brand_name',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('d_name', 'd_salary', 'company', 'license_info')
    search_fields = ('d_name', 'd_license')
    list_filter = ('company',)
    inlines = [DriverVehicleAssignmentInline]

    def license_info(self, obj):
        return obj.d_license

    license_info.short_description = 'Номер удостоверения'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('car_number', 'brand', 'company', 'active_driver_info', 'car_year')
    search_fields = ('car_number', 'brand__brand_name')
    list_filter = ('company', 'brand', 'car_year')
    inlines = [DriverVehicleAssignmentInline]

    def active_driver_info(self, obj):
        return obj.active_driver.d_name if obj.active_driver else '-'

    active_driver_info.short_description = 'Активный водитель'

    def save_model(self, request, obj, form, change):
        # Проверка при изменении предприятия
        if change and 'company' in form.changed_data and obj.drivers.exists():
            from django.core.exceptions import ValidationError
            raise ValidationError("Нельзя изменить предприятие, пока есть назначенные водители")
        super().save_model(request, obj, form, change)


@admin.register(DriverVehicleAssignment)
class DriverVehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'vehicle', 'assignment_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'vehicle__company')
    search_fields = ('driver__d_name', 'vehicle__car_number')

    def save_model(self, request, obj, form, change):
        # Проверка принадлежности к одному предприятию
        if obj.driver.company != obj.vehicle.company:
            from django.core.exceptions import ValidationError
            raise ValidationError("Водитель и автомобиль должны принадлежать одному предприятию")
        super().save_model(request, obj, form, change)