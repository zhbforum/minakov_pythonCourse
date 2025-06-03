from datetime import datetime, timezone
from db import db_connection
from utils.utils import get_exchange_rate
from utils.response_utils import api_response
from logger import logger
from constants import LOG_INFO, LOG_WARN, LOG_ERROR
from query.queries import (
    GET_ACCOUNT_BY_ID,
    UPDATE_ACCOUNT_BALANCE,
    GET_BANK_NAME_BY_ID,
    INSERT_TRANSACTION,
)


@db_connection
def transfer_money(sender_account_id: int, receiver_account_id: int, amount: float, currency: str, cursor=None) -> dict:
    logger.info("Initiating transfer of %s %s from account %s to %s", amount, currency, sender_account_id, receiver_account_id)

    sender = get_account_by_id(sender_account_id, cursor)
    receiver = get_account_by_id(receiver_account_id, cursor)

    if not sender or not receiver:
        return api_response(False, "Sender or receiver account not found.", log_type=LOG_WARN)

    if not has_sufficient_balance(sender, amount):
        return api_response(False, "Insufficient balance.", log_type=LOG_WARN)

    converted_amount = convert_currency_if_needed(amount, sender[2], receiver[2])  

    update_balances(cursor, sender[0], receiver[0], amount, converted_amount)  

    record_transaction(cursor, sender[3], sender[0], receiver[3], receiver[0], currency, amount)

    logger.info("Transferred %s %s from acc %s to %s", amount, currency, sender_account_id, receiver_account_id)
    return api_response(True, f"{amount} {currency} sent successfully.", log_type=LOG_INFO)


def get_account_by_id(account_id: int, cursor) -> tuple:
    cursor.execute(GET_ACCOUNT_BY_ID, (account_id,))
    return cursor.fetchone()  


def has_sufficient_balance(account: tuple, amount: float) -> bool:
    return account[1] >= amount  


def convert_currency_if_needed(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return amount
    rate = get_exchange_rate(from_currency, to_currency)
    return amount * rate


def update_balances(cursor, sender_id: int, receiver_id: int, amount: float, converted_amount: float):
    cursor.execute(UPDATE_ACCOUNT_BALANCE, (-amount, sender_id))
    cursor.execute(UPDATE_ACCOUNT_BALANCE, (converted_amount, receiver_id))


def record_transaction(
    cursor,
    sender_bank_id: int,
    sender_account_id: int,
    receiver_bank_id: int,
    receiver_account_id: int,
    currency: str,
    amount: float
):
    sender_bank_name = get_bank_name_by_id(cursor, sender_bank_id)
    receiver_bank_name = get_bank_name_by_id(cursor, receiver_bank_id)

    cursor.execute(INSERT_TRANSACTION, (
        sender_bank_name,
        sender_account_id,
        receiver_bank_name,
        receiver_account_id,
        currency,
        amount,
        datetime.now(timezone.utc).isoformat()
    ))


def get_bank_name_by_id(cursor, bank_id: int) -> str:
    cursor.execute(GET_BANK_NAME_BY_ID, (bank_id,))
    result = cursor.fetchone()
    return result[0] if result else "Unknown"
