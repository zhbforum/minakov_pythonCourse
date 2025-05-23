import os
import logging
import zipfile
from constants import ARCHIVE_EXTENSION, LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


def log_folder_structure(folder_path: str, indent: int = 0):
    """
    Recursively logs the structure of a folder using indentation.

    Args:
        folder_path (str): Path to the folder to be logged.
        indent (int): Indentation level for nested folders (used internally).
        
    Side effects:
        Logs the folder and file structure using the 'lab_3_logger'.
    """
    for entry in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, entry)
        prefix = "  " * indent
        if os.path.isdir(full_path):
            log.info(f"{prefix}[DIR] {entry}")
            log_folder_structure(full_path, indent + 1)
        else:
            log.info(f"{prefix}[FILE] {entry}")


def archive_folder(folder_path: str):
    """
    Create a ZIP archive of the specified folder.

    Args:
        folder_path (str): Path to the folder to be archived.

    Returns:
        str: Path to the created ZIP archive file.

    Side effects:
        Writes a ZIP file to disk.
        Logs the archive creation process using the 'lab_3_logger'.
    """
    zip_path = folder_path.rstrip("/\\") + ARCHIVE_EXTENSION
    log.info(f"Creating archive: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=folder_path)
                zipf.write(full_path, arcname)
    log.info("Archive created: " + zip_path)
    return zip_path
