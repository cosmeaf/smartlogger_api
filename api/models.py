from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def current_year():
    return date.today().year

class Device(models.Model):
    device_id = models.CharField(max_length=255, primary_key=True, unique=True)
    in_manutenance = models.BooleanField(default=False)
    hdr = models.CharField(max_length=255, verbose_name="Header", null=True, blank=True)
    report_map = models.CharField(max_length=255, verbose_name="Report Map", null=True, blank=True)
    model = models.CharField(max_length=255, verbose_name="Model", null=True, blank=True)
    software_version = models.CharField(max_length=50, verbose_name="Software Version", null=True, blank=True)
    message_type = models.CharField(max_length=50, verbose_name="Message Type", null=True, blank=True)
    date = models.DateField(verbose_name="Date", default=date.today, null=True, blank=True)
    time = models.TimeField(verbose_name="Time", null=True, blank=True)
    latitude = models.FloatField(verbose_name="Latitude", null=True, blank=True)
    longitude = models.FloatField(verbose_name="Longitude", null=True, blank=True)
    speed_gps = models.FloatField(verbose_name="Speed GPS (Km/h)", null=True, blank=True)
    course = models.CharField(max_length=50, verbose_name="Course", null=True, blank=True)
    satellites = models.IntegerField(verbose_name="Satellites", null=True, blank=True)
    gps_fix_status = models.CharField(max_length=50, verbose_name="GPS Fix Status", null=True, blank=True)
    input_state = models.CharField(max_length=255, verbose_name="Input State", null=True, blank=True)
    output_state = models.CharField(max_length=255, verbose_name="Output State", null=True, blank=True)
    data_length = models.IntegerField(verbose_name="Data Length", null=True, blank=True)
    driver_id = models.CharField(max_length=255, verbose_name="Driver ID", null=True, blank=True)
    instant_speed = models.FloatField(verbose_name="Instant Speed", null=True, blank=True)
    peak_speed = models.FloatField(verbose_name="Peak Speed", null=True, blank=True)
    instant_temperature = models.FloatField(verbose_name="Instant Temperature", null=True, blank=True)
    peak_temperature = models.FloatField(verbose_name="Peak Temperature", null=True, blank=True)
    mode = models.CharField(max_length=50, verbose_name="Mode", null=True, blank=True)
    report_type = models.CharField(max_length=50, verbose_name="Report Type", null=True, blank=True)
    message_number = models.CharField(max_length=50, verbose_name="Message Number", null=True, blank=True)
    reserved = models.CharField(max_length=255, verbose_name="Reserved", null=True, blank=True)
    assign_map = models.CharField(max_length=255, verbose_name="Assign Map", null=True, blank=True)
    power_voltage = models.FloatField(verbose_name="Power Voltage", null=True, blank=True)
    battery_voltage = models.FloatField(verbose_name="Battery Voltage", null=True, blank=True)
    connection_rat = models.CharField(max_length=50, verbose_name="Connection RAT", null=True, blank=True)
    acceleration_x = models.FloatField(verbose_name="Acceleration X", null=True, blank=True)
    acceleration_y = models.FloatField(verbose_name="Acceleration Y", null=True, blank=True)
    acceleration_z = models.FloatField(verbose_name="Acceleration Z", null=True, blank=True)
    adc_value = models.FloatField(verbose_name="ADC Value", null=True, blank=True)
    gps_odometer = models.FloatField(verbose_name="GPS Odometer", null=True, blank=True)
    trip_distance = models.FloatField(verbose_name="Trip Distance", null=True, blank=True)
    horimeter = models.FloatField(verbose_name="Horimeter", null=True, blank=True, default=0.0)
    trip_horimeter = models.FloatField(verbose_name="Trip Horimeter", null=True, blank=True)
    idle_time = models.FloatField(verbose_name="Idle Time", null=True, blank=True)
    impact = models.FloatField(verbose_name="Impact", null=True, blank=True)
    soc_battery_voltage = models.FloatField(verbose_name="SoC (Battery Voltage)", null=True, blank=True)
    calculated_temperature = models.FloatField(verbose_name="Calculated Temperature", null=True, blank=True)

    def __str__(self):
        return f"Device {self.device_id} - {self.model}"

    def update_hdr(self, new_hdr):
        try:
            # Se já existir algum valor em hdr
            if self.hdr:
                # Divide os valores existentes por vírgula e remove espaços extras
                existing_hdrs = [hdr.strip() for hdr in self.hdr.split(',')]
                
                # Se o novo valor não estiver na lista, o adiciona
                if new_hdr not in existing_hdrs:
                    existing_hdrs.append(new_hdr)
                    self.hdr = ','.join(existing_hdrs)
            else:
                # Se não houver valor em hdr, define diretamente o novo valor
                self.hdr = new_hdr

            # Salva as alterações no banco de dados
            self.save()

        except Exception as e:
            # Log detalhado para capturar o erro original
            logger.error(f"Failed to update HDR for device {self.device_id}. Error: {e}")
            raise ValueError(f"Failed to update HDR for device {self.device_id}. Original error: {e}") from e




class Equipment(models.Model):
    device = models.OneToOneField('Device', on_delete=models.CASCADE, related_name='equipments')
    in_manutenance = models.BooleanField(default=False)
    initial_hour_machine = models.FloatField('Initial Hour Machine', default=0)
    total_worked_hours = models.FloatField('Total Worked Hours', default=0, editable=False)
    remaining_hours = models.FloatField('Remaining Hours', default=0.0, editable=False)
    alarm_hours = models.FloatField('Alarm Hours', default=0.0)  # Pode ser editável
    name = models.CharField('Name', max_length=255)
    year = models.IntegerField('Year', blank=True, null=True, default=current_year)
    model = models.CharField('Model', max_length=255, default='N/A', blank=True, null=True)
    measuring_point = models.CharField('Measuring Point', max_length=255, default='N/A', blank=True, null=True)
    fuel = models.CharField('Fuel', max_length=8, default='DIESEL', blank=True, null=True)
    pulse_number = models.IntegerField('Pulse Number', default=0, blank=True, null=True)
    tire_perimeter = models.FloatField('Tire Perimeter (cm)', default=0.0, blank=True, null=True)
    available_hours_per_month = models.FloatField('Available Hours per Month', default=0.0, blank=True, null=True)
    average_consumption = models.FloatField('Average Consumption (m³/h - L/h - Kg/h)', default=0.0, blank=True, null=True)
    speed_alert = models.FloatField('Speed Alert (km/h)', default=0.0, blank=True, null=True)
    temperature_alert = models.FloatField('Temperature Alert (°C)', default=0.0, blank=True, null=True)
    shock_alert = models.FloatField('Shock Alert (km/h)', default=0.0, blank=True, null=True)
    effective_hours_odometer = models.CharField('Effective Hours or Odometer', max_length=255, default='ODOMETER', blank=True, null=True)
    odometer = models.FloatField('Odometer', default=0.0, blank=True, null=True)
    notes = models.TextField('Notes', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['device', 'name']),
        ]
        verbose_name_plural = "Equipment"
        verbose_name = "Equipment"

    def __str__(self):
        return f"{self.name} - {self.device.device_id}"


    def increment_worked_hours(self):
        """
        Incrementa as horas trabalhadas em 1 a cada atualização do horímetro Suntech.
        O valor do horímetro é tratado como um contador incremental, apenas para adicionar horas.
        """
        # Incrementa o total de horas trabalhadas em 1 a cada vez que o horímetro é atualizado
        self.total_worked_hours += 1
        logger.info(f"Horas trabalhadas incrementadas: {self.total_worked_hours}")

    def calculate_remaining_hours(self):
        """
        Calcula as horas restantes com base no alarme de horas e nas horas trabalhadas.
        """
        if self.alarm_hours > 0:
            self.remaining_hours = self.alarm_hours - self.total_worked_hours
        else:
            self.remaining_hours = self.total_worked_hours
        logger.info(f"Horas restantes calculadas: {self.remaining_hours}")
        return self.remaining_hours

    def save(self, *args, **kwargs):
        """
        Override do método save para calcular total_worked_hours e remaining_hours antes de salvar.
        """
        # Atualiza as horas trabalhadas (incrementa em 1 a cada vez que é chamado)
        self.increment_worked_hours()

        # Calcula as horas restantes
        self.calculate_remaining_hours()

        super().save(*args, **kwargs)



class Maintenance(models.Model):
    equipament = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='maintenances')
    horimetro_inicial_suntech = models.FloatField('Ajuste de Zero Hora Suntech', default=0)
    horimetro_inicial_maintenance = models.FloatField('AZ Hora Máquina', default=0)
    horimetro_acumulado = models.FloatField('Horímetro Acumulado', default=0)
    name = models.CharField(max_length=255)
    os = models.BooleanField(default=False)  # Status de Ordem de Serviço (em manutenção)
    usage_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    alarm_hours = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    obs = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['equipament']),
            models.Index(fields=['name']),
            models.Index(fields=['os']),
        ]
        verbose_name_plural = "Maintenance Records"
        verbose_name = "Maintenance Record"

    @property
    def horas_uso_peca(self):
        if self.equipament and self.equipament.device:
            hora_suntech = float(self.equipament.device.horimeter) - self.horimetro_inicial_suntech
            horas_uso_peca = Decimal(self.usage_hours) + Decimal(hora_suntech) + Decimal(self.horimetro_acumulado)
            return max(horas_uso_peca, Decimal(0))
        return Decimal(0)

    @property
    def remaining_hours(self):
        return self.alarm_hours - self.horas_uso_peca

    @property
    def background_color(self):
        color = ""
        if self.os:
            remaining_hours = self.remaining_hours
            if remaining_hours >= 0:
                color = ""
            elif remaining_hours >= -50:
                color = "bg-yellow-300"
            elif remaining_hours >= -100:
                color = "bg-orange-300"
            else:
                color = "bg-red-300"
        logger.debug(f"OS status: {self.os}, Background color: {color}")
        return color

    def atualizar_horimetro_acumulado(self):
        if self.equipament and self.equipament.device:
            self.horimetro_acumulado += float(self.equipament.device.horimeter) - self.horimetro_inicial_suntech
            self.horimetro_inicial_suntech = float(self.equipament.device.horimeter)
            self.save(update_fields=['horimetro_acumulado', 'horimetro_inicial_suntech'])

    def save(self, *args, **kwargs):
        # Quando salvar a manutenção, o horímetro Suntech atualiza normalmente
        if self.equipament and self.equipament.device:
            horimetro_atual = float(self.equipament.device.horimeter) if self.equipament.device.horimeter is not None else 0
            self.horimetro_inicial_suntech = horimetro_atual
            self.horimetro_inicial_maintenance = horimetro_atual

        # Atualiza os status de manutenção para Device e Equipment
        if self.equipament:
            self.equipament.in_manutenção = self.os  # Atualiza o status de manutenção no Equipment
            self.equipament.save(update_fields=['in_manutenção'])

            if self.equipament.device:
                self.equipament.device.in_manutenção = self.os  # Atualiza o status de manutenção no Device
                self.equipament.device.save(update_fields=['in_manutenção'])

        super().save(*args, **kwargs)

    def reset_usage_hours(self):
        self.usage_hours = Decimal(0)
        self.horimetro_inicial_suntech = self.equipament.device.horimeter if self.equipament and self.equipament.device else 0
        self.save(update_fields=['usage_hours', 'horimetro_inicial_suntech'])
