import os
import csv
import logging
from datetime import datetime
from collections import defaultdict, Counter
from constants import DATE_FMT_DOB, ERROR_INVALID_DOB, DATE_FMT_REG


log = logging.getLogger("lab_3_logger")

def get_decade(dob_str: str) -> str | None:
    """
    Convert a date of birth string to a decade string.

    Args:
        dob_str (str): Date of birth in the format specified by DATE_FMT_DOB.

    Returns:
        str or None: Decade label (e.g., '90-th') if year >= 1960, otherwise None.
    """
    try:
        year = datetime.strptime(dob_str, DATE_FMT_DOB).year
        if year < 1960:
            return None
        decade = (year // 10) * 10
        return f"{str(decade)[-2:]}-th"
    except Exception as e:
        log.warning(ERROR_INVALID_DOB.format(dob_str, e))
        return None


def calculate_age(dob_str: str) -> int:
    """
    Calculate the current age based on a date of birth string.

    Args:
        dob_str (str): Date of birth in the format specified by DATE_FMT_DOB.

    Returns:
        int: Age in years.
    """
    dob = datetime.strptime(dob_str, DATE_FMT_DOB)
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def calculate_years_since(date_str: str) -> float:
    """
    Calculate the number of years since a given date string.

    Args:
        date_str (str): Date in the format specified by DATE_FMT_REG.

    Returns:
        float: Number of years since the given date, rounded to one decimal place.
    """
    parsed_date = datetime.strptime(date_str, DATE_FMT_REG)
    now = datetime.today()
    return round((now - parsed_date).days / 365.25, 1)


def organize_and_save(data: list[dict], base_path: str):
    """
    Organize user data by decade and country, compute statistics,
    and save grouped results into CSV files.

    Args:
        data (list[dict]): List of user records.
        base_path (str): Base directory path to save organized CSV files.

    Side effects:
        Creates directories and writes CSV files to disk.
        Logs actions and warnings using the 'lab_3_logger'.
    """
    log.info("Organizing data by decade and country...")

    grouped = defaultdict(list)

    for row in data:
        decade = get_decade(row["dob.date"])
        if not decade:
            continue

        try:
            age = calculate_age(row["dob.date"])
            reg_years = calculate_years_since(row["registered.date"])
        except Exception as e:
            log.warning(f"Skipping row due to error: {e}")
            continue

        row["decade"] = decade
        row["age"] = age
        row["reg_years"] = reg_years

        country = row["location.country"]
        grouped[(decade, country)].append(row)

    for (decade, country), group_rows in grouped.items():
        dir_path = os.path.join(base_path, decade, country)
        os.makedirs(dir_path, exist_ok=True)

        max_age, total_reg, id_counter = 0, 0, Counter()
        for row in group_rows:
            max_age = max(max_age, row["age"])
            total_reg += row["reg_years"]
            id_counter[row["id.name"]] += 1

        avg_reg = round(total_reg / len(group_rows), 1)
        popular_id = id_counter.most_common(1)[0][0]

        filename = f"max_age_{max_age}_avg_registered_{avg_reg}_popular_id_{popular_id}.csv"
        file_path = os.path.join(dir_path, filename)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=group_rows[0].keys())
            writer.writeheader()
            writer.writerows(group_rows)

        log.info(f"Saved group to: {file_path}")
