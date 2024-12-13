import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Configuración desde el .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BACKUP_FOLDER = os.getenv("BACKUP_FOLDER")
TEMP_BACKUP_PATH = os.getenv("TEMP_BACKUP_PATH")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")