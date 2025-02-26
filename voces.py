import requests

# Tu API Key de Eleven Labs
API_KEY = "tu_api_key_aquí"

# Endpoint para obtener las voces
url = "https://api.elevenlabs.io/v1/voices"

# Headers con la API Key
headers = {
    "xi-api-key": "sk_e356f8e5ca4e61fc2abdeb4e034b98e0447d51663fde8dcc"
}

# Hacer la solicitud GET
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    voices = response.json()["voices"]
    
    # Filtrar las voces en español
    spanish_voices = []
    for voice in voices:
        if "es" in voice.get("labels", {}).get("language", ""):
            spanish_voices.append(voice)
    
    # Mostrar las voces en español
    print(f"Voces en español encontradas: {len(spanish_voices)}")
    for voice in spanish_voices:
        print(f"Nombre: {voice['name']}, ID: {voice['voice_id']}")
else:
    print(f"Error: {response.status_code} - {response.text}")