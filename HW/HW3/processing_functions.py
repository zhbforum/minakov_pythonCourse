import logging
import csv
from datetime import datetime, timedelta, timezone
from dateutil import parser
from constants import DATE_FMT_DOB, DATE_FMT_REG, TITLE_MAP, ERROR_INVALID_TIMEZONE, DEFAULT_TIMEZONE, DATE_FMT_CURRENT, LOGGER_NAME


log = logging.getLogger(LOGGER_NAME)


def convert_title(title: str) -> str:
    """
    Convert a formal title to its normalized form using TITLE_MAP.

    Args:
        title (str): Original title from the dataset.

    Returns:
        str: Normalized title if found in TITLE_MAP, otherwise the original title.
    """
    return TITLE_MAP.get(title, title)


def calculate_current_time(timezone_offset: str) -> str:
    """
    Calculate the current UTC time adjusted by the given timezone offset.

    Args:
        timezone_offset (str): Timezone offset in format "+HH:MM" or "-HH:MM".

    Returns:
        str: Adjusted current time as a formatted string (YYYY-MM-DD HH:MM:SS),
             or an empty string if parsing fails.
    """

    try:
        hours, minutes = map(int, timezone_offset.replace("+", "")
                             .replace("-", "").split(":"))
        delta = timedelta(hours=hours, minutes=minutes) 
        sign = 1 if timezone_offset.startswith("+") else -1
        now = datetime.now(timezone.utc) + delta * sign
        return now.strftime(DATE_FMT_CURRENT)
    except Exception as e:
        log.warning(ERROR_INVALID_TIMEZONE.format(timezone_offset, e))
        return DEFAULT_TIMEZONE


def format_date(date_str: str, fmt: str) -> str:
    return parser.parse(date_str).strftime(fmt)


def process_row(row: dict, index: int) -> dict | None:
    """
    Process a single row from the CSV file by enriching and formatting its fields.

    Adds a global index, normalizes the title, formats dates, and calculates the current time
    based on the timezone offset.

    Args:
        row (dict): A dictionary representing a single CSV row with user data.
        index (int): The zero-based index of the row in the dataset.

    Returns:
        dict | None: Updated row with additional and formatted fields, or None if processing fails.
    """
    try:
        row["global_index"] = index + 1
        row["name_title"] = convert_title(row["name.title"])
        row["dob.date"] = format_date(row["dob.date"]).strftime(DATE_FMT_DOB)
        row["registered.date"] = format_date(row["registered.date"]).strftime(DATE_FMT_REG)
        row["current_time"] = calculate_current_time(row["location.timezone.offset"])
        return row
    except Exception as e:
        log.warning(f"Skipping row {index} due to error: {e}")
        return None


def process_csv(file_path: str) -> list[dict]:
    """
    Read and process a CSV file containing user data.

    Reads the file, converts each row using `process_row`, and collects all successfully
    processed rows into a list.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list[dict]: A list of processed rows, each represented as a dictionary.
    """
    log.info(f"Processing CSV file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)       
        processed_rows = [
            processed for i, row in enumerate(reader)
            if (processed := process_row(row, i))
        ]
    log.info(f"Processed {len(processed_rows)} rows.")
    return processed_rows
