# from tabnanny import verbose
#
# from django.db import models
# from django.db.models import AutoField
#
#
# class Vehicle(models.Model):
#     car_id = models.AutoField(primary_key = True, verbose_name = "ID")
#     car_number = models.CharField(max_length = 10, default = '', verbose_name = "Номер автомобиля")
#     car_cost = models.IntegerField(verbose_name = "Цена")
#     car_year = models.IntegerField(verbose_name = "Год выпуска")
#     car_mileage = models.IntegerField(verbose_name = "Пробег")
#     car_color = models.CharField(verbose_name = "Цвет")
#
#     brand = models.ForeignKey("Brand", on_delete = models.SET_DEFAULT, default = 0,
#                               related_name='+', verbose_name = "ID Брэнда")
#     company = models.ForeignKey("Enterprise", on_delete = models.SET_NULL)
#
#     class Meta:
#         ordering = ['car_id']
#         verbose_name = 'Автомобиль'
#         verbose_name_plural = 'Автомобили'
#
#     def __str__(self):
#         return str(self.car_id)
#
#
# brand_name_choices = (
#     ('1', 'Легковой'),
#     ('2', 'Грузовой'),
#     ('3', 'Автобус'),
#     ('4', 'Мотоцикл'),
#     ('5', 'Трактор'),
#     ('6', 'Noname')
# )
#
# class Brand(models.Model):
#     brand_id = models.AutoField(primary_key = True, verbose_name = "ID")
#     brand_name = models.CharField(choices = brand_name_choices, blank = True)
#     brand_tonnage = models.IntegerField(verbose_name = "Грузоподъемность, кг", blank = True)
#     brand_places = models.IntegerField(verbose_name = "Количество сидячих мест", blank = True)
#     brand_tank = models.IntegerField(verbose_name = "Объем бака, л", blank = True)
#     brand_door = models.IntegerField(default = '3', verbose_name = "Количество дверей", blank = True)
#
#     class Meta:
#         ordering = ['brand_id']
#         verbose_name = 'Брэнд'
#         verbose_name_plural = 'Брэнды'
#
#     def __str__(self):
#         return str(self.brand_id)
#
#
# class Driver(models.Model):
#     d_id = AutoField(primary_key = True, verbose_name = 'ID')
#     d_name = models.CharField(max_length = 30, default = '', verbose_name = "ФИО водителя")
#     d_salary = models.IntegerField(verbose_name = 'Зарплата')
#
#     company = models.ForeignKey("Enterprise", on_delete = models.SET_NULL)
#     vehicle = models.ManyToManyField("vehicle", on_delete = models.SET_NULL)
#
#     class Meta:
#         ordering = ['d_id']
#         verbose_name = 'Водитель'
#         verbose_name_plural = 'Водители'
#
#     def __str__(self):
#         return str(self.d_id)
#
# class Enterprise(models.Model):
#     e_id = AutoField(primary_key = True, verbose_name = 'ID')
#     e_name = models.CharField(max_length = 20, verbose_name = 'Название предприятния')
#     e_city = models.CharField(max_length = 20, verbose_name = 'Город нахождения')
#
#     class Meta:
#         ordering = ['e_id']
#         verbose_name = 'Компания'
#         verbose_name_plural = 'Компании'
#
#     def __str__(self):
#         return str(self.e_id)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import AutoField


class Vehicle(models.Model):
    car_id = models.AutoField(primary_key=True, verbose_name="ID")
    car_number = models.CharField(max_length=10, default='', verbose_name="Номер автомобиля")
    car_cost = models.IntegerField(verbose_name="Цена")
    car_year = models.IntegerField(verbose_name="Год выпуска")
    car_mileage = models.IntegerField(verbose_name="Пробег")
    car_color = models.CharField(verbose_name="Цвет")
    active_driver = models.OneToOneField(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_vehicle',
        verbose_name="Активный водитель"
    )

    brand = models.ForeignKey(
        "Brand",
        on_delete=models.SET_DEFAULT,
        default=0,
        verbose_name="ID Брэнда"
    )
    company = models.ForeignKey(
        "Enterprise",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Предприятие"
    )

    class Meta:
        ordering = ['car_id']
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.car_number} ({self.brand})"

    def save(self, *args, **kwargs):
        # Проверка, что активный водитель принадлежит тому же предприятию
        if self.active_driver and self.active_driver.company != self.company:
            raise ValueError("Активный водитель должен принадлежать тому же предприятию")
        super().save(*args, **kwargs)


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True, verbose_name="ID")
    brand_name = models.CharField(max_length=50, verbose_name="Название бренда")
    brand_tonnage = models.IntegerField(verbose_name="Грузоподъемность, кг", blank=True, null=True)
    brand_places = models.IntegerField(verbose_name="Количество сидячих мест", blank=True, null=True)
    brand_tank = models.IntegerField(verbose_name="Объем бака, л", blank=True, null=True)
    brand_door = models.IntegerField(default=3, verbose_name="Количество дверей", blank=True, null=True)

    class Meta:
        ordering = ['brand_id']
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __str__(self):
        return self.brand_name


class Driver(models.Model):
    d_id = AutoField(primary_key=True, verbose_name='ID')
    d_name = models.CharField(max_length=30, default='', verbose_name="ФИО водителя")
    d_salary = models.IntegerField(verbose_name='Зарплата')
    d_license = models.CharField(max_length=20, verbose_name='Номер водительского удостоверения', blank=True)

    company = models.ForeignKey(
        "Enterprise",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Предприятие"
    )
    vehicles = models.ManyToManyField(
        "Vehicle",
        through='DriverVehicleAssignment',
        related_name='drivers',
        verbose_name="Автомобили"
    )

    class Meta:
        ordering = ['d_id']
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.d_name


class DriverVehicleAssignment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    assignment_date = models.DateField(auto_now_add=True, verbose_name="Дата назначения")
    is_active = models.BooleanField(default=False, verbose_name="Активное назначение")

    class Meta:
        unique_together = [['driver', 'vehicle']]
        verbose_name = 'Назначение водителя'
        verbose_name_plural = 'Назначения водителей'

    def save(self, *args, **kwargs):
        # Проверка, что водитель и автомобиль принадлежат одному предприятию
        if self.driver.company != self.vehicle.company:
            raise ValueError("Водитель и автомобиль должны принадлежать одному предприятию")

        # Если это активное назначение, снимаем активность с других назначений этого водителя
        if self.is_active:
            DriverVehicleAssignment.objects.filter(
                driver=self.driver,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
            self.vehicle.active_driver = self.driver
            self.vehicle.save()

        super().save(*args, **kwargs)


class Enterprise(models.Model):
    e_id = AutoField(primary_key=True, verbose_name='ID')
    e_name = models.CharField(max_length=20, verbose_name='Название предприятия')
    e_city = models.CharField(max_length=20, verbose_name='Город нахождения')
    e_address = models.CharField(max_length=50, verbose_name='Адрес', blank=True)

    class Meta:
        ordering = ['e_id']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f"{self.e_name} ({self.e_city})"


