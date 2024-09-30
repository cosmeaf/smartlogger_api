from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    total_hour_meter = forms.CharField(
        label='Horímetro Total',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    class Meta:
        model = Equipment
        fields = [
            'device',
            'initial_hour_device',
            'initial_hour_machine',
            'name',
            'year',
            'model',
            'measuring_point',
            'fuel',
            'pulse_number',
            'tire_perimeter',
            'available_hours_per_month',
            'average_consumption',
            'speed_alert',
            'temperature_alert',
            'shock_alert',
            'effective_hours_odometer',
            'odometer',
            'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2100, 'class': 'form-control'}),
            'initial_hour_device': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'initial_hour_machine': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'tire_perimeter': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'available_hours_per_month': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'average_consumption': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'speed_alert': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'temperature_alert': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'shock_alert': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
            'odometer': forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'}),
        }
        labels = {
            'initial_hour_device': 'Ajuste de Zero Hora Suntech',
            'initial_hour_machine': 'AZ Hora Máquina',
            'total_hour_meter': 'Horímetro Total',
            'name': 'Nome',
            'year': 'Ano',
            'model': 'Modelo',
            'measuring_point': 'Ponto de Medição',
            'fuel': 'Combustível',
            'pulse_number': 'Número de Pulsos',
            'tire_perimeter': 'Perímetro do Pneu (cm)',
            'available_hours_per_month': 'Horas Disponíveis por Mês',
            'average_consumption': 'Consumo Médio (m³/h - L/h - Kg/h)',
            'speed_alert': 'Alerta de Velocidade (km/h)',
            'temperature_alert': 'Alerta de Temperatura (°C)',
            'shock_alert': 'Alerta de Shock (km/h)',
            'effective_hours_odometer': 'Horas Efetivas ou Hodômetro',
            'odometer': 'Hodômetro',
            'notes': 'Observações'
        }
        help_texts = {
            'year': 'Digite o ano do equipamento.',
            'notes': 'Digite qualquer observação adicional aqui.',
        }
        error_messages = {
            'name': {
                'max_length': 'O nome do equipamento é muito longo.',
            },
            'odometer': {
                'invalid': 'Digite um valor numérico válido para o hodômetro.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['total_hour_meter'].initial = self.instance.total_hour_meter
        # Aplicar a classe 'form-control' a todos os campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
