import os
import requests
from bs4 import BeautifulSoup

# URL base e diretório de destino
base_url = "https://injetec.com.br/assets/imgs/clientes/"
output_dir = "/root/projects/django/django_smartlogger/static/linux/images/clientes"

# Cria o diretório de saída, se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Obtém a lista de imagens dinamicamente do servidor
response = requests.get(base_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

# Loop para encontrar e baixar cada imagem na lista
for link in soup.find_all('a'):
    img_name = link.get('href')
    if img_name.endswith(('.jpg', '.png', '.jpeg')):
        img_url = base_url + img_name
        img_path = os.path.join(output_dir, img_name)

        try:
            img_data = requests.get(img_url, verify=False).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {img_name}")
        except Exception as e:
            print(f"Failed to download {img_name}: {e}")

print("Todos os downloads foram concluídos.")
