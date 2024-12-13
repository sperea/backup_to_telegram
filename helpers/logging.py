import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("backup_to_telegram.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("BackupToTelegram")

def get_logger():
    return logging.getLogger("BackupToTelegram")
