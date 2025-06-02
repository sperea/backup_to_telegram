# This script implements the requested functionality: creating a backup, splitting it into parts under 2GB, encrypting it, and uploading it to Telegram.

import os
import argparse
import glob
from helpers.compression import compress_and_encrypt
from helpers.telegram import async_send_to_telegram
from helpers.logging import setup_logger
import asyncio

# Setup logger
logger = setup_logger()

def split_file(file_path, max_size_mb):
    """Split a file into parts of max_size_mb."""
    part_size = max_size_mb * 1024 * 1024
    with open(file_path, 'rb') as f:
        part_number = 0
        while chunk := f.read(part_size):
            part_file = f"{file_path}.part{part_number}"
            with open(part_file, 'wb') as part_f:
                part_f.write(chunk)
            part_number += 1

    return sorted(glob.glob(f"{file_path}.part*"))

def main():
    parser = argparse.ArgumentParser(description="Backup folder to Telegram.")
    parser.add_argument('--backup-folder', required=True, help="Path to the folder to backup.")
    parser.add_argument('--temp-backup-path', required=True, help="Path to store temporary backup files.")
    parser.add_argument('--encryption-key', help="GPG key ID for encryption.")
    parser.add_argument('--password', help="Password for encryption (alternative to GPG key).")

    args = parser.parse_args()

    if not args.encryption_key and not args.password:
        parser.error("You must provide either --encryption-key or --password for encryption.")

    # Compress and encrypt the folder
    backup_file = compress_and_encrypt(
        folder_path=args.backup_folder,
        output_dir=args.temp_backup_path,
        encryption_key=args.encryption_key,
        password=args.password
    )

    # Split the file into parts under 2GB
    logger.info("Splitting the backup file into parts under 2GB...")
    part_files = split_file(backup_file, max_size_mb=2000)

    # Upload parts to Telegram
    logger.info("Uploading parts to Telegram...")
    asyncio.run(async_send_to_telegram(part_files))

if __name__ == "__main__":
    main()
