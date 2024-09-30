# utils/location/get_location_info.py
from decouple import config
import requests
import logging

logger = logging.getLogger(__name__)

API_KEY = config('API_KEY')

def get_location_info(ip_address):
    try:
        logger.info(f"Tentando obter informações de localização para o IP: {ip_address}")
        response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip_address}')
        data = response.json()
        
        if response.status_code == 200:
            location_info = {
                "ip": ip_address,
                "isp": data.get("isp", "Desconhecido"),
                "country": data.get("country_name", "Desconhecido"),
                "state": data.get("state_prov", "Desconhecido"),
                "city": data.get("city", "Desconhecido"),
                "zipcode": data.get("zipcode", "Desconhecido"),
            }
            logger.info(f"Informações de localização obtidas com sucesso: {location_info}")
            return location_info
        else:
            logger.error(f"API de geolocalização retornou código de erro: {response.status_code}")
            return {"error": "API returned an error code"}
    
    except Exception as e:
        logger.error(f"Erro ao obter informações de geolocalização para o IP {ip_address}: {str(e)}")
        return {"error": str(e)}
