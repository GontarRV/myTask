from django.urls import path
from .views import ViewEnterprise, IndexEnterprises, LoginManager, Menu

app_name = 'manager'  # Добавляем namespace

urlpatterns = [
    path('login/', LoginManager.as_view(), name='login'),
    path('menu/', Menu.as_view(), name='menu'),
    path('enterprises/', IndexEnterprises.as_view(), name='manager_enterprises'),
    path('enterprises/<str:name>', ViewEnterprise.as_view(), name='enterprise')
]