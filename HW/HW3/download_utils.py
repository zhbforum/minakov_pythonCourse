import requests
import logging
import os
from constants import BASE_URL, MAX_ROWS, CSV_FORMAT, LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


def download_users_csv(filename: str, dest_folder: str, gender: str = None, rows: int = MAX_ROWS):
    """
    Download user data from randomuser.me API in CSV format and save it to a file.

    Args:
        filename (str): Name of the output CSV file (without extension).
        dest_folder (str): Destination folder path to save the file.
        gender (str, optional): Optional gender filter ('male' or 'famale'). Defaults to None.
        rows (int): Number of rows to download. Defaults to MAX_ROWS.

    Returns:
        str: Full path to the saved CSV file.

    Raises:
        requests.RequestException: If there is an error during the API request.

    Side effects:
        Sends HTTP GET request to the randomuser.me API.
        Saves the response content as a CSV file in the specified destination folder.
        Logs the process using the 'lab_3_logger'.
    """
    if rows > MAX_ROWS:
        log.warning(f"API supports up to {MAX_ROWS} rows; trimming to limit.")
        rows = MAX_ROWS

    params = {
        "results": rows,
        "format": CSV_FORMAT
    }
    if gender:
        params["gender"] = gender

    log.info(f"Requesting {rows} users from randomuser.me...")
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        log.error(f"Error downloading data: {e}")
        raise 

    full_filename = os.path.join(dest_folder, f"{filename}.{CSV_FORMAT}")
    with open(full_filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    log.info(f"CSV saved successfully as: {full_filename}")
    return full_filename
