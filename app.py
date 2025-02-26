""" from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from typing import Dict, List
import requests
import uuid
import os

# API Keys
OPENROUTER_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_e356f8e5ca4e61fc2abdeb4e034b98e0447d51663fde8dcc"

# Inicializar cliente OpenAI con OpenRouter
client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

app = FastAPI()

# Almacenar contexto de chat por usuario
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# Modelo de solicitud para chat
class ChatRequest(BaseModel):
    session_id: str
    question: str

# Función para obtener historial de una sesión
def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []  # Nueva sesión
    return chat_sessions[session_id]

# Función para generar audio con ElevenLabs
def generate_audio(session_id: str, text: str):
    elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"  # ID de voz (puedes cambiarlo)
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }

    # Solicitar audio a ElevenLabs
    response = requests.post(elevenlabs_url, json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al generar audio")

    # Guardar el archivo de audio
    audio_filename = f"response_{session_id}.mp3"
    with open(audio_filename, "wb") as f:
        f.write(response.content)

    return audio_filename

# Endpoint para recibir preguntas, responder y generar audio
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        history = get_chat_history(request.session_id)

        # Agregar la nueva pregunta al historial
        history.append({"role": "user", "content": request.question})

        # Limitar historial a las últimas 2 interacciones (4 mensajes en total)
        history = history[-4:]  
        chat_sessions[request.session_id] = history  

        # Incluir un mensaje de sistema para respuestas concisas
        messages = [{"role": "system", "content": "Responde de forma breve y precisa. No expliques tu razonamiento."}] + history

        # Llamar a la API de OpenRouter
        chat_response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=messages
        )

        # Obtener respuesta y agregarla al historial
        bot_response = chat_response.choices[0].message.content
        history.append({"role": "assistant", "content": bot_response})

        # Generar el audio
        audio_filename = generate_audio(request.session_id, bot_response)

        # Devolver la respuesta y la URL del audio
        print(f"/audio/{request.session_id}")
        return {
            "response": bot_response,
            "audio_url": f"/audio/{request.session_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para servir el archivo de audio
@app.get("/audio/{session_id}")
async def get_audio(session_id: str):
    audio_filename = f"response_{session_id}.mp3"
    
    if not os.path.exists(audio_filename):
        raise HTTPException(status_code=404, detail="Audio no encontrado")

    return FileResponse(audio_filename, media_type="audio/mpeg", filename="response.mp3")

# Generar un nuevo session_id
@app.get("/new_session")
async def new_session():
    session_id = str(uuid.uuid4())  
    chat_sessions[session_id] = []  
    return {"session_id": session_id}
 """
 
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
import requests
import uuid
import os

# API Keys
OPENROUTER_API_KEY = "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"
ELEVENLABS_API_KEY = "sk_e356f8e5ca4e61fc2abdeb4e034b98e0447d51663fde8dcc"
CLOUDINARY_URL = "https://api.cloudinary.com/v1_1/ddm9rclrt/upload"
CLOUDINARY_API_KEY = "289967145513177"
CLOUDINARY_API_SECRET = "OHLUT8lFf4497i5MWxJNhw4FGWg"

# Inicializar cliente OpenAI con OpenRouter
client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes. Puedes cambiarlo a ["http://localhost:8081"] si solo quieres permitir tu frontend.
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Almacenar contexto de chat por usuario
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# Modelo de solicitud para chat
class ChatRequest(BaseModel):
    session_id: str
    question: str

# Función para obtener historial de una sesión
def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []  # Nueva sesión
    return chat_sessions[session_id]

# Función para generar audio con ElevenLabs
def generate_audio(session_id: str, text: str):
    print(text)
    elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"  # ID de voz
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }

    # Solicitar audio a ElevenLabs
    response = requests.post(elevenlabs_url, json=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al generar audio")

    # Guardar el archivo de audio localmente
    audio_filename = f"response_{session_id}.mp3"
    with open(audio_filename, "wb") as f:
        f.write(response.content)

    return audio_filename

# Función para subir audio a Cloudinary
def upload_to_cloudinary(file_path: str):
    with open(file_path, "rb") as file:
        response = requests.post(
            CLOUDINARY_URL,
            files={"file": file},
            data={
                "upload_preset": "unsigned_preset",  # Asegúrate de que este preset exista en Cloudinary
                "api_key": CLOUDINARY_API_KEY  # Cloudinary NO requiere api_secret en uploads
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error al subir audio a Cloudinary: {response.text}")

    return response.json().get("secure_url", "")

# Endpoint para recibir preguntas, responder y generar audio
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        history = get_chat_history(request.session_id)

        # Agregar la nueva pregunta al historial
        history.append({"role": "user", "content": request.question})

        # Limitar historial a las últimas 2 interacciones (4 mensajes en total)
        history = history[-4:]  
        chat_sessions[request.session_id] = history  

        # Incluir un mensaje de sistema para respuestas concisas
        messages = [{"role": "system", "content": "Responde de forma breve y precisa en español. No expliques tu razonamiento."}] + history

        # Llamar a la API de OpenRouter
        chat_response = client.chat.completions.create(
            model ="google/gemini-2.0-flash-thinking-exp:free",
            messages=messages,
             extra_body={
             "models": [  # Modelos de respaldo en caso de fallo
            "deepseek/deepseek-r1:free",
            "meta-llama/llama-3.2-11b-vision-instruct:free"
        ]
    }
        )

        # Obtener respuesta y agregarla al historial
        bot_response = chat_response.choices[0].message.content
        history.append({"role": "assistant", "content": bot_response})

        # Generar el audio
        audio_filename = generate_audio(request.session_id, bot_response)

        # Subir el audio a Cloudinary
        cloudinary_url = upload_to_cloudinary(audio_filename)

        # Eliminar el archivo local después de subirlo
        os.remove(audio_filename)

        # Devolver la respuesta y la URL del audio
        return {
            "response": bot_response,
            "audio_url": cloudinary_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generar un nuevo session_id
@app.get("/new_session")
async def new_session():
    session_id = str(uuid.uuid4())  
    chat_sessions[session_id] = []  
    return {"session_id": session_id}
 

# python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
# https://chatbot-voz-production.up.railway.app/
