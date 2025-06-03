# from django.urls import include, path
# from rest_framework import routers
# from . import views
#
# router = routers.DefaultRouter()
# router.register(r'vehicle', views.VehicleViewSet)
# router.register(r'brand', views.BrandViewSet)
#
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('CarPark-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'enterprises', views.EnterpriseViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'assignments', views.DriverVehicleAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('CarPark-auth/', include('rest_framework.urls', namespace='rest_framework'))
]