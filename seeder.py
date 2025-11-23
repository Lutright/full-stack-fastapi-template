import requests
import random
from faker import Faker

# Configuración
API_URL = "http://167.172.10.152:8000/api/v1"
NUM_ITEMS = 5000  # ¡Ajusta esto para más carga!
EMAIL = "admin@example.com" # Usuario por defecto del template
PASSWORD = "changethis"     # Contraseña por defecto del template

fake = Faker()

def get_token():
    """Obtiene el token de acceso (Login)"""
    response = requests.post(
        f"{API_URL}/login/access-token",
        data={"username": EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Error al loguearse:", response.text)
        exit()

def create_items(token):
    """Genera items masivamente"""
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Iniciando la creación de {NUM_ITEMS} items...")
    
    for i in range(NUM_ITEMS):
        item_data = {
            "title": fake.sentence(nb_words=4),
            "description": fake.text(max_nb_chars=100)
        }
        resp = requests.post(f"{API_URL}/items/", json=item_data, headers=headers)
        
        if i % 100 == 0:
            print(f"Progreso: {i}/{NUM_ITEMS} items creados.")

if __name__ == "__main__":
    print("Esperando a que la API esté lista...")
    try:
        token = get_token()
        create_items(token)
        print("¡Carga de datos completada con éxito!")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        print("Asegúrate de que Docker Compose esté corriendo (Paso 3).")