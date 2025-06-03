from typing import Union
from db import db_connection
from logger import logger
from utils.response_utils import api_response
from constants import LOG_INFO, LOG_WARN, LOG_ERROR


@db_connection
def update_info(table_name: str, id_field: str, id_value: Union[int, str], fields: dict, cursor=None) -> dict:
    if not fields:
        return api_response(False, "No fields provided for update", log_type=LOG_WARN)

    set_clause = ", ".join([f"{key} = %s" for key in fields])
    values = list(fields.values()) + [id_value]
    query = f'UPDATE "{table_name}" SET {set_clause} WHERE {id_field} = %s'

    cursor.execute(query, values)

    if cursor.rowcount == 0:
        return api_response(False, f"No rows updated in {table_name} with {id_field} = {id_value}", log_type=LOG_WARN)

    return api_response(True, f"Updated {cursor.rowcount} row(s) in {table_name}", log_type=LOG_INFO)


@db_connection
def delete_info(table_name: str, criteria: dict, cursor=None) -> dict:
    if not criteria:
        return api_response(False, "No criteria provided for deletion", log_type=LOG_WARN)

    conditions = " AND ".join([f"{key} = %s" for key in criteria])
    values = list(criteria.values())
    query = f'DELETE FROM "{table_name}" WHERE {conditions}'

    cursor.execute(query, values)

    if cursor.rowcount == 0:
        return api_response(False, f"No rows deleted from {table_name} matching {criteria}", log_type=LOG_WARN)

    return api_response(True, f"{cursor.rowcount} row(s) deleted from {table_name}", log_type=LOG_INFO)


def add_objects(
    cursor,
    table: str,
    fields: list[str],
    prepared_items: list[tuple],
    entity_name: str,
    skipped: int = 0
) -> dict:
    inserted_ids = []
    placeholders = ", ".join(["%s"] * len(fields))
    field_str = ", ".join(fields)
    query = f'INSERT INTO "{table}" ({field_str}) VALUES ({placeholders}) RETURNING id'

    for row in prepared_items:
        try:
            cursor.execute(query, row)
            inserted_ids.append(cursor.fetchone()[0])
        except Exception as e:
            logger.warning("Skipping row %s for table %s: %s", row, table, e)
            skipped += 1

    logger.info("Inserted %d %s(s), skipped %d", len(inserted_ids), entity_name, skipped)

    return api_response(
        True,
        f"Inserted {len(inserted_ids)} {entity_name}(s), skipped {skipped}",
        data=inserted_ids,
        log_type=LOG_INFO
    )


def update_object(
    table: str,
    id_value: int,
    updates: dict,
    id_field: str = "id",
    entity_name: str = None
) -> dict:
    entity_name = entity_name or table
    logger.info("Updating %s with %s = %s, fields: %s", entity_name, id_field, id_value, updates)

    result = update_info(table, id_field, id_value, updates)
    return api_response(
        result["status"] == "success",
        result["message"],
        data=result.get("data"),
        log_type=LOG_INFO if result["status"] == "success" else LOG_WARN
    )


def delete_object(
    table: str,
    id_value: int,
    id_field: str = "id",
    entity_name: str = None
) -> dict:
    entity_name = entity_name or table
    logger.info("Deleting %s with %s = %s", entity_name, id_field, id_value)

    result = delete_info(table, {id_field: id_value})
    return api_response(
        result["status"] == "success",
        result["message"],
        data=result.get("data"),
        log_type=LOG_INFO if result["status"] == "success" else LOG_WARN
    )
