from django.contrib import admin
from .models import Manager
from CarPark.models import Enterprise


@admin.register(Manager)
class AdminManager(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company']

    def company(self, obj):
        return tuple(Enterprise.objects.filter(manager=obj))