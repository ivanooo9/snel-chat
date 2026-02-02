import os
import re

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not found. Relying on system environment variables.")

# ========================
# FLASK & SECURITY
# ========================
SECRET_KEY = os.getenv("SECRET_KEY", "default_insecure_key_change_me")
FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = FLASK_ENV == "development"
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

# ========================
# DATABASE
# ========================
DB_PATH = "chatbot.db"

# ========================
# APPSHEET
# ========================
APPSHEET_APP_ID = os.getenv("APPSHEET_APP_ID", "")
APPSHEET_KEY = os.getenv("APPSHEET_KEY", "")
APPSHEET_RETRIES = 3
APPSHEET_TIMEOUT = 10
APPSHEET_TEST_PHONE = "+593000000000"

# ========================
# CALENDAR
# ========================
CALENDAR_ID = os.getenv("CALENDAR_ID", "") # Optionally load from env if needed for reference, but mostly used in Service Logic checking logic
# The Calendar Service uses a service account file
SERVICE_ACCOUNT_FILE = 'credentials.json'
GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = 'America/Guayaquil'

# ========================
# ASSETS
# ========================
ONBOARDING_VIDEO_URL = os.getenv("ONBOARDING_VIDEO_URL", "")

# ========================
# CONSTANTS & CATALOGS
# ========================
COVERED_SECTORS = [
    "Epoca", "Operadores", "Chontacruz", "Colinas Lojanas", "Daniel Alvarez", "Zarzas I", "Zarzas II",
    "Sol de los Andes", "Esteban Godoy", "Ciudad Alegria", "Argelia", "Los Cipres", "San Isidro",
    "El Electricista", "Union Lojana", "Los Geranios", "La Pradera", "Pucara", "Los Cocos",
    "Tebaida", "San Pedro"
]

def normalize(text):
    if not text: return ""
    text = re.sub(r'[^\w\s]', '', text) 
    replacements = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
        ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U")
    )
    for a, b in replacements:
        text = text.replace(a, b)
    return text.lower().strip()

NORMALIZED_SECTORS = {normalize(s): s for s in COVERED_SECTORS}

PRODUCT_CATALOG = {
    # Cameras
    "cam_ext_wifi": {"desc": "Cámara IP Exterior Wi-Fi Full HD con Visión Nocturna", "val": 45, "cat": "Cámaras"},
    "cam_ext_cable": {"desc": "Cámara Hikvision Turbo HD 4.0 Exterior (Cableada)", "val": 35, "cat": "Cámaras"},
    "cam_int_wifi": {"desc": "Cámara Robótica Interior 360° Wi-Fi", "val": 30, "cat": "Cámaras"},
    "cam_int_cable": {"desc": "Cámara Domo Interior HD 1080p", "val": 28, "cat": "Cámaras"},
    
    # Videoporteros
    "video_casa": {"desc": "Videoportero Analógico Kit Hogar", "val": 120, "cat": "Videoporteros"},
    "video_negocio": {"desc": "Videoportero IP Multi-usuario para Edificios", "val": 250, "cat": "Videoporteros"},
    
    # Alarmas
    "alarma_casa": {"desc": "Kit Alarma Inalámbrica Básica (Sensor Puerta + Movimiento)", "val": 85, "cat": "Alarmas"},
    "alarma_negocio": {"desc": "Central de Alarma Híbrida 8 Zonas Profesional", "val": 180, "cat": "Alarmas"},
    
    # Cerraduras
    "cerradura_casa": {"desc": "Cerradura Inteligente Huella/Clave para Puerta Principal", "val": 150, "cat": "Cerraduras"},
    "cerradura_negocio": {"desc": "Control de Acceso Biométrico para Personal", "val": 200, "cat": "Cerraduras"},
    
    # Energia
    "ups_casa": {"desc": "UPS 500VA para Router y PC Básico", "val": 45, "cat": "Respaldo Energía"},
    "ups_negocio": {"desc": "UPS Online 1KVA Doble Conversión", "val": 300, "cat": "Respaldo Energía"},
}
