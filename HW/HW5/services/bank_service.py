from typing import Union
from utils.utils import load_csv_to_dicts
from utils.response_utils import api_response
from logger import logger
from services.generic_service import add_objects, update_object, delete_object
from constants import BANK_FIELDS, LOG_ERROR


def prepare_bank(bank: dict) -> tuple[str]:
    name = bank["name"]
    return (name,)


def add_bank(*banks: Union[dict, list[dict]]) -> dict:
    return add_objects( # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        table="Bank",
        fields=BANK_FIELDS,
        raw_items=banks,
        prepare_func=prepare_bank,
        entity_name="bank"
    )


def update_bank(bank_id: int, fields: dict) -> dict:
    updates = {k: v for k, v in fields.items() if k in BANK_FIELDS}
    return update_object(
        table="Bank",
        id_value=bank_id,
        updates=updates,
        entity_name="bank"
    )


def delete_bank(bank_id: int) -> dict:
    return delete_object(
        table="Bank",
        id_value=bank_id,
        entity_name="bank"
    )


def add_bank_from_csv(path: str) -> dict:
    try:
        data = load_csv_to_dicts(path)
        result = add_bank(data)
        logger.info("CSV import from %s: %s", path, result['message'])
        return result
    except Exception as e:
        logger.error("CSV import from %s failed: %s", path, e)
        return api_response(False, f"CSV import from {path} failed: {e}", log_type=LOG_ERROR)
