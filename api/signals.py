from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Device, Equipment, Maintenance
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Device)
def update_equipment_calculations(sender, instance, **kwargs):
    """
    Signal que recalcula worked_hours para o equipamento relacionado
    toda vez que o horímetro do dispositivo é atualizado.
    """
    try:
        # Tenta obter o equipamento relacionado ao dispositivo
        try:
            equipment = Equipment.objects.get(device=instance)
            
            # Recalcula worked_hours para o equipamento baseado no incremento do horímetro
            equipment.worked_hours = equipment.get_worked_hours()
            equipment.save()

            logger.info(f"Equipment '{equipment.name}' updated with worked_hours: {equipment.worked_hours}")

        except Equipment.DoesNotExist:
            logger.warning(f"Equipment related to device '{instance.device_id}' not found.")

    except Exception as e:
        logger.error(f"Error updating worked_hours for device {instance.device_id}: {str(e)}")



@receiver(post_save, sender=Device)
def update_maintenance_hours(sender, instance, **kwargs):
    try:
        # Obtém o equipamento relacionado ao dispositivo atualizado
        equipment = Equipment.objects.get(device=instance)
        
        # Itera sobre as manutenções relacionadas para recalcular as horas
        for maintenance in Maintenance.objects.filter(equipment=equipment):
            # Atualiza worked_hours e remaining_hours para cada manutenção
            maintenance.worked_hours = maintenance.get_worked_hours()
            maintenance.remaining_hours = maintenance.get_remaining_hours()
            maintenance.save()

            # Log para verificar as atualizações
            logger.info(f"Atualizado '{maintenance.name}' com worked_hours: {maintenance.worked_hours} e remaining_hours: {maintenance.remaining_hours}")

    except Equipment.DoesNotExist:
        logger.warning(f"Equipamento para dispositivo '{instance.id}' não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao atualizar manutenções para dispositivo {instance.id}: {str(e)}")
