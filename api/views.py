from rest_framework import viewsets, mixins
from .models import Device, Equipment, Maintenance
from .serializers import DeviceSerializer, EquipmentSerializer, MaintenanceSerializer

class DeviceViewSet(mixins.ListModelMixin, 
                    mixins.RetrieveModelMixin, 
                    viewsets.GenericViewSet):
    """
    ViewSet apenas para leitura. Permite listar e recuperar detalhes dos dispositivos.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all().order_by('id')
    serializer_class = EquipmentSerializer


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer