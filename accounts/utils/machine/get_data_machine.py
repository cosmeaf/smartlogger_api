# utils/machine/get_data_machine.py
import platform
import distro
import logging

logger = logging.getLogger(__name__)

def get_machine_info():
    try:
        system_info = {
            "os_name": platform.system(),
            "os_version": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        
        # Detectar se é uma distribuição Linux
        if system_info["os_name"].lower() == "linux":
            distro_name = distro.name(pretty=True) or "Desconhecido"
            distro_version = distro.version(pretty=True) or "Desconhecido"
            system_info["linux_distro"] = distro_name
            system_info["linux_distro_version"] = distro_version
        elif system_info["os_name"].lower() == "darwin":
            system_info["os_name"] = "MacOS"
        
        logger.info(f"Informações da máquina obtidas: {system_info}")
        return system_info

    except Exception as e:
        logger.error(f"Erro ao obter informações da máquina: {str(e)}")
        return {"error": str(e)}

