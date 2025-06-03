import random
from datetime import datetime, timezone, timedelta

from db import db_connection
from logger import logger
from query.queries import (
    GET_USERS_WITH_DEBTS,
    GET_BANK_WITH_BIGGEST_CAPITAL,
    GET_OLDEST_USER_BANK,
    GET_MOST_UNIQUE_SENDERS_BANK,
    GET_ALL_USER_IDS,
    DELETE_INCOMPLETE_USERS,
    DELETE_INCOMPLETE_ACCOUNTS,
    GET_LAST_3_MONTH_TRANSACTIONS,
    GET_ACCOUNT_IDS_BY_USER_ID,
    GET_CURRENCY_STATS
)
from utils.response_utils import api_response
from constants import LOG_INFO, LOG_WARN


@db_connection
def assign_random_discounts(cursor=None) -> dict:
    logger.info("Selecting users for random discounts")

    cursor.execute(GET_ALL_USER_IDS)
    user_ids = [row[0] for row in cursor.fetchall()]

    if not user_ids:
        return api_response(False, "No users found for random discounts", data=[], log_type=LOG_WARN)

    selected = random.sample(user_ids, min(len(user_ids), 10))
    discounts = {user_id: random.choice([25, 30, 50]) for user_id in selected}

    return api_response(True, f"Discounts assigned to {len(discounts)} users", data=discounts, log_type=LOG_INFO)


@db_connection
def get_users_with_debts(cursor=None) -> dict:
    cursor.execute(GET_USERS_WITH_DEBTS)
    results = cursor.fetchall()

    if not results:
        return api_response(True, "No users with debts found", data=[], log_type=LOG_INFO)

    full_names = [f"{name} {surname}" for name, surname in results]
    return api_response(True, f"Found {len(full_names)} users with debts", data=full_names, log_type=LOG_INFO)


@db_connection
def get_bank_with_biggest_capital(cursor=None) -> dict:
    cursor.execute(GET_BANK_WITH_BIGGEST_CAPITAL)
    result = cursor.fetchone()

    if not result:
        return api_response(True, "No banks found with capital", data=None, log_type=LOG_WARN)

    bank_name, capital = result
    return api_response(
        True,
        f"Bank '{bank_name}' has the biggest capital: {capital}",
        data={"bank": bank_name, "total_capital": float(capital)},
        log_type=LOG_INFO
    )


@db_connection
def get_bank_with_oldest_user(cursor=None) -> dict:
    logger.info("Searching for bank with oldest user")

    cursor.execute(GET_OLDEST_USER_BANK)
    result = cursor.fetchone()

    if not result:
        return api_response(False, "No user with birth_day found", data=None, log_type=LOG_WARN)

    return api_response(True, f"Bank '{result[0]}' has the oldest user", data={"bank_name": result[0]}, log_type=LOG_INFO)


@db_connection
def get_bank_with_most_unique_senders(cursor=None) -> dict:
    logger.info("Calculating bank with most unique outbound transaction users")

    cursor.execute(GET_MOST_UNIQUE_SENDERS_BANK)
    result = cursor.fetchone()

    if not result:
        return api_response(False, "No outbound transactions found", data=None, log_type=LOG_WARN)

    bankname, user_count = result
    return api_response(
        True,
        f"Bank '{bankname}' has the most unique senders: {user_count}",
        data={"bank": bankname, "unique_senders": user_count},
        log_type=LOG_INFO
    )


@db_connection
def cleanup_incomplete_data(cursor=None) -> dict:
    logger.info("Deleting users with missing name, surname or accounts fields")

    cursor.execute(DELETE_INCOMPLETE_USERS)
    deleted_users = cursor.rowcount

    cursor.execute(DELETE_INCOMPLETE_ACCOUNTS)
    deleted_accounts = cursor.rowcount

    return api_response(
        True,
        "Deleted incomplete users and accounts",
        data={"users_deleted": deleted_users, "accounts_deleted": deleted_accounts},
        log_type=LOG_INFO
    )


@db_connection
def get_user_transactions_last_3_months(user_id: int, cursor=None) -> dict:
    logger.info("Fetching transactions for user_id=%s in last 3 months", user_id)

    cursor.execute(GET_ACCOUNT_IDS_BY_USER_ID, (user_id,))
    account_ids = [row[0] for row in cursor.fetchall()]

    if not account_ids:
        return api_response(False, f"No accounts found for user_id={user_id}", data=[], log_type=LOG_WARN)

    three_months_ago = datetime.now(timezone.utc) - timedelta(days=90)
    cursor.execute(GET_LAST_3_MONTH_TRANSACTIONS, (account_ids, three_months_ago.isoformat()))
    transactions = cursor.fetchall()

    if not transactions:
        return api_response(True, "No transactions in the last 3 months", data=[], log_type=LOG_INFO)

    return api_response(True, f"{len(transactions)} transactions found", data=transactions, log_type=LOG_INFO)


@db_connection
def get_currency_transfer_stats(cursor=None) -> dict:
    logger.info("Fetching currency usage statistics")

    cursor.execute(GET_CURRENCY_STATS)
    results = cursor.fetchall()
    stats = dict(results)

    return api_response(True, "Currency usage statistics retrieved successfully", data=stats, log_type=LOG_INFO)
