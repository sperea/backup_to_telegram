import os
import subprocess
import datetime
from helpers.logging import get_logger

logger = get_logger()

def compress_and_encrypt(folder_path, output_dir, encryption_key, max_size_mb=48):
    try:
        # Asegurarse de que la carpeta de salida existe
        os.makedirs(output_dir, exist_ok=True)

        # Crear nombre único para el archivo con extensión .tar.gpg
        fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = os.path.join(output_dir, f"backup_{fecha}.tar.gpg")

        logger.info(f"Respaldo será guardado en: {backup_file}")
        print(f"[INFO] Respaldo será guardado en: {backup_file}")

        # Comprimir y cifrar la carpeta
        command = f"tar -cf - {folder_path} | gpg --encrypt --recipient '{encryption_key}' -o {backup_file}"
        logger.info("Ejecutando comando de compresión y cifrado...")
        subprocess.run(command, shell=True, check=True)

        # Dividir el archivo en partes de máximo tamaño especificado (en MB)
        part_prefix = os.path.join(output_dir, f"backup_{fecha}.tar.gpg.part.")
        split_command = f"split -b {max_size_mb}M -d {backup_file} {part_prefix}"
        logger.info("Dividiendo el archivo en partes de máximo 2GB...")
        print("[INFO] Dividiendo el archivo en partes de máximo 2GB...")
        subprocess.run(split_command, shell=True, check=True)

        # Eliminar el archivo original después de dividirlo
        os.remove(backup_file)

        logger.info(f"Respaldo dividido en partes: {part_prefix}*")
        return part_prefix
    except subprocess.CalledProcessError as e:
        logger.error(f"Error durante la compresión, cifrado o división: {e}")
        print(f"[ERROR] Error durante la compresión, cifrado o división: {e}")
        return None
