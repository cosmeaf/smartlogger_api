from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Device, Equipment
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Device)
def update_equipment_hours_before_save(sender, instance, **kwargs):
    """
    Signal que é chamado toda vez que o Device é salvo.
    Atualiza as horas trabalhadas e as horas restantes no Equipment relacionado,
    antes de salvar os dados no banco.
    """
    try:
        # Verifica se o equipamento está associado a esse dispositivo
        equipment = Equipment.objects.get(device=instance)
        
        logger.info(f'Atualizando horas do equipamento relacionado ao dispositivo {instance.device_id}')
        
        # O método save() no Equipment já cuida de incrementar as horas e calcular o restante
        equipment.save()

        logger.info(f'Atualização de horas concluída para o equipamento {equipment.id}')

    except Equipment.DoesNotExist:
        logger.warning(f'Equipamento relacionado ao dispositivo {instance.device_id} não encontrado.')
    except Exception as e:
        logger.error(f'Erro ao atualizar horas do equipamento: {e}')
        raise ValueError(f"Failed to update equipment hours for device {instance.device_id}. Original error: {e}") from e
