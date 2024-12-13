import asyncio
import sys
import glob
from telegram import Bot
from telegram.request import HTTPXRequest
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from helpers.logging import get_logger

logger = get_logger()

async def async_send_to_telegram(part_files):
    try:
        # Aumentar significativamente los timeouts.
        # Por ejemplo: 300 segundos (5 minutos).
        request = HTTPXRequest(read_timeout=60000.0, connect_timeout=60000.0)
        bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request)

        for part in sorted(part_files):
            retries = 0
            success = False
            while retries < 3:
                try:
                    with open(part, "rb") as file:
                        logger.info(f"Enviando archivo: {part}")
                        await bot.send_document(chat_id=TELEGRAM_CHAT_ID, document=file)
                    logger.info(f"Archivo enviado exitosamente: {part}")
                    print(f"[INFO] Archivo enviado: {part}")
                    success = True
                    break
                except Exception as e:
                    retries += 1
                    logger.warning(f"Reintentando {part}, intento {retries}/3, Error: {e}")
                    print(f"[WARNING] Reintentando {part}, intento {retries}/3")

            if not success:
                logger.error(f"Fallo al enviar {part} después de 3 intentos.")
                print(f"[ERROR] Fallo al enviar {part} después de 3 intentos.")
                sys.exit(1)  # Salir con error si falla

        logger.info("Todos los archivos se enviaron exitosamente.")
        print("[INFO] Todos los archivos se enviaron exitosamente.")

    except Exception as e:
        logger.error(f"Error crítico enviando los archivos a Telegram: {e}")
        print(f"[ERROR] Error crítico enviando los archivos a Telegram: {e}")
        sys.exit(1)

def send_to_telegram(file_prefix):
    part_files = glob.glob(f"{file_prefix}*")
    asyncio.run(async_send_to_telegram(part_files))
