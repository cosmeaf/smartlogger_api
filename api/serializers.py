from rest_framework import serializers
from .models import Device, Equipment, Maintenance, MaintenanceResetLog, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    
    def create(self, validated_data):
        equipment = validated_data.pop('equipment', None)
        employee = Employee.objects.create(**validated_data)
        return employee
    
    
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'



class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = '__all__' 


class MaintenanceResetLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceResetLog
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.maintenance:
            representation['maintenance'] = instance.maintenance.name
        return representation