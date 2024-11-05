import json
import random
import requests
import shutil

def load_lines_from_file(url):
    """Load lines from a given URL."""
    response = requests.get(url)
    return response.text.strip().split('\n')

# URLs de los archivos
json_url = 'https://raw.githubusercontent.com/vsh00t/SliverConfig/refs/heads/main/http-c2.json'
extensions_url = 'https://raw.githubusercontent.com/vsh00t/SliverConfig/refs/heads/main/extensions.txt'
servers_url = 'https://raw.githubusercontent.com/vsh00t/SliverConfig/refs/heads/main/servers.txt'
cookies_url = 'https://raw.githubusercontent.com/vsh00t/SliverConfig/refs/heads/main/cookies.txt'
agents_url = 'https://raw.githubusercontent.com/vsh00t/SliverConfig/refs/heads/main/agents.txt'

# Cargar datos desde los archivos
extensions = load_lines_from_file(extensions_url)
servers = load_lines_from_file(servers_url)
cookies = load_lines_from_file(cookies_url)
agents = load_lines_from_file(agents_url)

# Cargar el archivo JSON original
response = requests.get(json_url)
data = json.loads(response.text)

def replace_values(obj):
    """Recursively replace specific values in the JSON structure."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                # Reemplazar extensiones
                if value.startswith('.'):
                    obj[key] = random.choice(extensions)
                # Reemplazar cookies
                elif 'cookie' in key.lower():
                    obj[key] = random.choice(cookies)
                # Reemplazar user agents
                elif 'agent' in key.lower():
                    obj[key] = random.choice(agents)
            elif isinstance(value, dict) or isinstance(value, list):
                replace_values(value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and item.get('name') == 'Server':
                item['value'] = random.choice(servers)
            else:
                replace_values(item)

# Reemplazar valores en el JSON
replace_values(data)

# Ruta del archivo original y respaldo
original_file_path = '/root/.sliver/configs/http-c2.json'
backup_file_path = '/root/.sliver/configs/http-c2-backup.json'

# Realizar un respaldo del archivo original
shutil.copyfile(original_file_path, backup_file_path)
print(f"Respaldo realizado: {backup_file_path}")

# Guardar el nuevo JSON en la ubicación original
with open(original_file_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"El archivo JSON ha sido modificado y guardado en '{original_file_path}'.")
