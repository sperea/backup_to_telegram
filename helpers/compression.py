import os
import subprocess
import datetime
from helpers.logging import get_logger

logger = get_logger()

def compress_and_encrypt(folder_path, output_dir, encryption_key=None, password=None, max_size_mb=48):
    try:
        # Asegurarse de que la carpeta de salida existe
        os.makedirs(output_dir, exist_ok=True)

        # Crear nombre único para el archivo de respaldo con extensión .tar.gpg o .tar.gz
        fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if password:
            backup_file = os.path.join(output_dir, f"backup_{fecha}.tar.gz")
        else:
            backup_file = os.path.join(output_dir, f"backup_{fecha}.tar.gpg")

        logger.info(f"Respaldo será guardado en: {backup_file}")
        print(f"[INFO] Respaldo será guardado en: {backup_file}")

        # Comprimir y cifrar la carpeta
        if password:
            command = f"tar -cf - {folder_path} | gzip | openssl enc -aes-256-cbc -salt -k '{password}' -out {backup_file}"
        else:
            command = f"tar -cf - {folder_path} | gpg --encrypt --recipient '{encryption_key}' -o {backup_file}"

        subprocess.run(command, shell=True, check=True)

        return backup_file
    except Exception as e:
        logger.error(f"Error durante la compresión y cifrado: {e}")
        print(f"[ERROR] Error durante la compresión y cifrado: {e}")
        raise
