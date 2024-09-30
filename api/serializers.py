from rest_framework import serializers
from .models import Device, Equipment, Maintenance

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'



class MaintenanceSerializer(serializers.ModelSerializer):
    horas_uso_peca = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_hours = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    background_color = serializers.CharField(read_only=True)
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = Maintenance
        fields = '__all__'