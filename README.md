  Backup to Telegram

Backup to Telegram
==================

A Python script to create encrypted backups of a specified folder, split them into manageable parts, and send them to a Telegram chat using the Telegram Bot API.

Features
--------

*   Encrypts backups using **GPG public key encryption**.
*   Splits large files into smaller parts to meet Telegram's API limits.
*   Automated retries for failed uploads.
*   Customizable backup directories and encryption configurations.

Requirements
------------

*   Python 3.12.2 or higher
*   `gpg` (GnuPG) installed on your system
*   Telegram Bot API token
*   Public GPG key for encryption

Limitations
-----------

*   Telegram's API limit for uploading files via bots is **50MB** for direct uploads.
*   Files larger than 50MB are uploaded as documents using the split functionality (default split size is 50Mb).
*   Ensure your internet connection is stable for uploading large files.

Usage
-----

    python backup_to_telegram.py --backup-folder <path_to_folder> --temp-backup-path <path_to_backup_directory> --encryption-key <gpg_key_id>

### Arguments

*   `--backup-folder`: Path to the folder you want to back up.
*   `--temp-backup-path`: Path to the directory where the backup files will be saved.
*   `--encryption-key`: GPG public key identifier for encryption.

Encryption Details
------------------

*   Uses **GPG public key encryption** for secure backups.
*   Ensure the recipient's public key is available and correctly configured in GPG.

Splitting Files
---------------

*   Default split size is **2GB**. This can be customized in the script.
*   Files are named using the format `backup_YYYY-MM-DD_HH-MM-SS.tar.gpg.part.XX`.
*   Parts are uploaded individually to Telegram.

Error Handling
--------------

*   Automatic retries for failed uploads (up to 3 attempts).
*   The script exits with an error code if any file fails to upload after retries.

Installation
------------

    pip install -r requirements.txt

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
------------

Contributions are welcome! Feel free to fork this repository and submit pull requests.

Contact
-------

For any issues or feature requests, please open an issue on the GitHub repository.