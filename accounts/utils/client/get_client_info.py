from user_agents import parse
import logging

logger = logging.getLogger(__name__)

def get_client_info(request=None):
    try:
        if request:
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)

            client_info = {
                "os_name": user_agent.os.family,
                "os_version": user_agent.os.version_string,
                "browser": user_agent.browser.family,
                "browser_version": user_agent.browser.version_string,
                "device": user_agent.device.family,
                "device_type": "Mobile" if user_agent.is_mobile else "Desktop"
            }
            logger.info(f"Informações do cliente obtidas: {client_info}")
        else:
            client_info = {
                "os_name": None,
                "os_version": None,
                "browser": None,
                "device": None,
                "device_type": None
            }

        return client_info

    except Exception as e:
        logger.error(f"Erro ao obter informações do cliente: {str(e)}")
        return {"error": str(e)}
