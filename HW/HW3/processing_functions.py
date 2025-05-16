import logging
import csv
from datetime import datetime, timedelta, timezone
from dateutil import parser
from constants import DATE_FMT_DOB, DATE_FMT_REG, TITLE_MAP, ERROR_INVALID_TIMEZONE, DEFAULT_TIMEZONE, DATE_FMT_CURRENT


log = logging.getLogger("lab_3_logger")


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
        hours, minutes = map(int, timezone_offset.replace(
            "+", "").replace("-", "").split(":"))
        delta = timedelta(hours=hours, minutes=minutes)
        now = datetime.now(timezone.utc)
        if timezone_offset.startswith("-"):
            now -= delta
        else:
            now += delta
        return now.strftime(DATE_FMT_CURRENT)
    except Exception as e:
        log.warning(ERROR_INVALID_TIMEZONE.format(timezone_offset, e))
        return DEFAULT_TIMEZONE


def process_csv(file_path: str) -> list[dict]:
    """
    Read and process a CSV file with user data.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        list[dict]: List of dictionaries representing processed rows.
        
    Side effects:
        Parses and rewrites dates and timezone data.
        Logs processing steps and row-level warnings.
    """
    log.info(f"Processing CSV file: {file_path}")
    processed_rows = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                row["global_index"] = i + 1
                row["name_title"] = convert_title(row["name.title"])
                row["dob.date"] = parser.parse(row["dob.date"]).strftime(DATE_FMT_DOB)
                row["registered.date"] = parser.parse(
                    row["registered.date"]).strftime(DATE_FMT_REG)
                row["current_time"] = calculate_current_time(
                    row["location.timezone.offset"])
                processed_rows.append(row)
            except Exception as e:
                log.warning(f"Skipping row {i} due to error: {e}")
                
    log.info(f"Processed {len(processed_rows)} rows.")
    return processed_rows
