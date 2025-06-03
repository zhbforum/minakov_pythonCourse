import re
from datetime import datetime, timezone
from constants import (
    ALLOWED_ACCOUNT_TYPES,
    ALLOWED_ACCOUNT_STATUSES,
    ALLOWED_CURRENCIES,
    ACCOUNT_NUMBER_PREFIX,
    ACCOUNT_NUMBER_LENGTH,
    ACCOUNT_NUMBER_INVALID_CHARS,
    ACCOUNT_NUMBER_REPLACEMENT_CHAR,
    ACCOUNT_NUMBER_PATTERN,
    FULL_NAME_CLEAN_PATTERN
)


def validate_enum_field(value: str, allowed: set, field_name: str):
    if value not in allowed:
        raise ValueError(f"Not allowed value '{value}' for field '{field_name}'!")


def validate_account_type(account_type: str):
    validate_enum_field(account_type, ALLOWED_ACCOUNT_TYPES, "type")


def validate_account_status(status: str):
    validate_enum_field(status, ALLOWED_ACCOUNT_STATUSES, "status")


def validate_currency(currency: str):
    validate_enum_field(currency, ALLOWED_CURRENCIES, "currency")


def validate_full_name(full_name: str) -> tuple[str, str]:
    clean = re.sub(FULL_NAME_CLEAN_PATTERN, "", full_name).strip()
    parts = clean.split()

    if len(parts) < 2:
        raise ValueError("Full name must contain at least name and surname!")

    return parts[0], parts[1]


def validate_account_number(number: str) -> str:
    number = re.sub(ACCOUNT_NUMBER_INVALID_CHARS, ACCOUNT_NUMBER_REPLACEMENT_CHAR, number)

    if len(number) != ACCOUNT_NUMBER_LENGTH:
        raise ValueError(f"account_number must be exactly {ACCOUNT_NUMBER_LENGTH} characters long!")

    if not number.startswith(ACCOUNT_NUMBER_PREFIX):
        raise ValueError(f"Wrong format! Must start with '{ACCOUNT_NUMBER_PREFIX}'")

    if not re.search(ACCOUNT_NUMBER_PATTERN, number):
        raise ValueError("Broken ID! Must contain pattern like j3-432547-")

    return number


def get_current_utc_time() -> str:
    return datetime.now(timezone.utc).isoformat()
