from typing import Union
from logger import logger
from db import db_connection
from validator import (
    validate_account_number,
    validate_account_type,
    validate_account_status,
    validate_currency,
)
from utils.utils import load_csv_to_dicts, normalize_items
from utils.response_utils import api_response
from services.generic_service import add_objects, update_object, delete_object
from constants import ACCOUNT_FIELDS, LOG_ERROR


def prepare_account(account: dict) -> tuple:
    user_id = account["user_id"]
    bank_id = account["bank_id"]
    acc_type = account["type"]
    acc_number = account["account_number"]
    currency = account["currency"]
    amount = account["amount"]
    status = account.get("status")

    validate_account_type(acc_type)
    if status:
        validate_account_status(status)
    validate_currency(currency)
    acc_number = validate_account_number(acc_number)

    return user_id, acc_type, acc_number, bank_id, currency, amount, status


@db_connection
def add_account(*accounts: Union[dict, list[dict]], cursor=None) -> dict:
    items = normalize_items(*accounts)
    cursor.execute("SELECT account_number FROM Account")
    existing_numbers = {row[0] for row in cursor.fetchall()}

    prepared = []
    skipped = 0

    for acc in items:
        if acc["account_number"] in existing_numbers:
            logger.warning("Skipping duplicate account_number: %s", acc["account_number"])
            skipped += 1
            continue
        try:
            prepared.append(prepare_account(acc))
        except Exception as e:
            logger.warning("Skipping account %s: %s", acc, e)
            skipped += 1

    return add_objects(
        cursor=cursor,
        table="Account",
        fields=ACCOUNT_FIELDS,
        prepared_items=prepared,
        entity_name="account",
        skipped=skipped
    )


def update_account(account_id: int, fields: dict) -> dict:
    updates = {k: v for k, v in fields.items() if k in ACCOUNT_FIELDS}

    if "type" in updates:
        validate_account_type(updates["type"])
    if "status" in updates:
        validate_account_status(updates["status"])
    if "currency" in updates:
        validate_currency(updates["currency"])
    if "account_number" in updates:
        updates["account_number"] = validate_account_number(updates["account_number"])

    return update_object(
        table="Account",
        id_value=account_id,
        updates=updates,
        entity_name="account"
    )


def delete_account(account_id: int) -> dict:
    return delete_object(
        table="Account",
        id_value=account_id,
        entity_name="account"
    )


def add_account_from_csv(path: str) -> dict:
    try:
        data = load_csv_to_dicts(path)
        result = add_account(data)
        logger.info("CSV import from %s: %s", path, result['message'])
        return result
    except Exception as e:
        logger.error("CSV import from %s failed: %s", path, e)
        return api_response(False, f"CSV import from {path} failed: {e}", log_type=LOG_ERROR)
