from typing import Any
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView
from CarPark.models import Vehicle
from CarPark.models import Enterprise
from manager.models import Manager
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import ManagerSerializer
from CarPark.serializers import EnterpriseSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class ManagerEnterpriseViewSet(viewsets.ModelViewSet):
    serializer_class = EnterpriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только предприятия текущего менеджера
        if hasattr(self.request.user, 'manager'):
            return self.request.user.manager.enterprises.all()
        return Enterprise.objects.none()

@method_decorator(csrf_protect, name='dispatch')
class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # Для админов - всех менеджеров, для остальных - только себя
        if self.request.user.is_staff:
            return Manager.objects.all()
        return Manager.objects.filter(id=self.request.user.manager.id)

@method_decorator(csrf_protect, name='dispatch')
class LoginManager(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manager/login.html', context={'username': ''})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and Manager.objects.filter(pk=user.pk).exists():
            login(request, user)
            return HttpResponseRedirect(reverse('manager:menu'))  # используем namespace:name
        else:
            return render(request, 'manager/login.html',
                          context={'username': username,
                                   'error': 'Неверные данные или вы не менеджер'})

@method_decorator(csrf_protect, name='dispatch')
class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manager/menu.html')

@method_decorator(csrf_protect, name='dispatch')
class IndexEnterprises(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(getattr(user, 'manager', None), Manager):
            user = request.user
            enterprises = Enterprise.objects.filter(manager=user)
            return render(request,
                          'manager/index_enterprise.html',
                          context={'enterprises': enterprises,
                                   'manager': user})

        return HttpResponseForbidden('Необходима аутентификация в качестве \
менеджера\n')

@method_decorator(csrf_protect, name='dispatch')
class ViewEnterprise(ListView):
    paginate_by = 5
    model = Vehicle
    template_name = 'manager/enterprise.html'
    enterprise = None

    def get(self, request, *args, **kwargs):
        v = Vehicle.objects.all()[0]
        response = super().get(request, *args, **kwargs)
        ViewEnterprise.enterprise = kwargs['name']
        response.context_data['enterprise'] = ViewEnterprise.enterprise
        return response

    def get_queryset(self):
        return Vehicle.objects.filter(enterprise__name=ViewEnterprise.enterprise)