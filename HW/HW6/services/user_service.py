from typing import Union
from utils.utils import load_csv_to_dicts, normalize_items
from utils.response_utils import api_response
from logger import logger
from validator import validate_full_name
from services.generic_service import add_objects, update_object, delete_object
from constants import USER_FIELDS, LOG_ERROR


def prepare_user(user: dict) -> tuple:
    name, surname = validate_full_name(user["user_full_name"])
    accounts = user.get("accounts")
    if not accounts:
        raise ValueError("Field 'accounts' is required for user.")
    birth_day = user.get("birth_day", None)
    return name, surname, birth_day, accounts


def add_user(cursor, *users: Union[dict, list[dict]]) -> dict:
    items = normalize_items(*users)
    try:
        prepared = [prepare_user(user) for user in items]
    except Exception as e:
        return api_response(False, f"Failed to prepare user data: {e}", log_type=LOG_ERROR)

    return add_objects(
        cursor=cursor,
        table="User",
        fields=USER_FIELDS,
        prepared_items=prepared,
        entity_name="user"
    )


def update_user(user_id: int, fields: dict) -> dict:
    updates = {}
    if "user_full_name" in fields:
        updates["name"], updates["surname"] = validate_full_name(fields["user_full_name"])
    for key in ("birth_day", "accounts"):
        if key in fields:
            updates[key] = fields[key]

    return update_object(
        table="User",
        id_value=user_id,
        updates=updates,
        entity_name="user"
    )


def delete_user(user_id: int) -> dict:
    return delete_object(
        table="User",
        id_value=user_id,
        entity_name="user"
    )


def add_user_from_csv(path: str) -> dict:
    try:
        data = load_csv_to_dicts(path)
        result = add_user(data)
        logger.info("CSV import from %s: %s", path, result['message'])
        return result
    except Exception as e:
        logger.error("CSV import from %s failed: %s", path, e)
        return api_response(False, f"CSV import from {path} failed: {e}", log_type=LOG_ERROR)
