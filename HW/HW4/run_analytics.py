from api import (
    assign_random_discounts,
    get_users_with_debts,
    get_bank_with_biggest_capital,
    get_bank_with_oldest_user,
    get_bank_with_most_unique_senders,
    cleanup_incomplete_data,
    get_user_transactions_last_3_months,
    get_currency_transfer_stats
)
from logger import logger


def run_analytics():
    tasks = [
        ("Assign random discounts", assign_random_discounts),
        ("Get users with debts", get_users_with_debts),
        ("Get bank with biggest capital", get_bank_with_biggest_capital),
        ("Get bank with oldest user", get_bank_with_oldest_user),
        ("Get bank with most unique senders", get_bank_with_most_unique_senders),
        ("Cleanup incomplete users/accounts", cleanup_incomplete_data),
        ("Get user transactions for last 3 months (user_id=1)", lambda: get_user_transactions_last_3_months(1)),
        ("Get currency transfer stats", get_currency_transfer_stats)
    ]

    for description, func in tasks:
        try:
            logger.info("Running task: %s", description)
            result = func()
            logger.info("Result of '%s': %s", description, result)
            print(f"{description}:\n{result}\n")
        except Exception as e:
            logger.error("Error in '%s': %s", description, e)
            print(f"Error in {description}: {e}\n")


if __name__ == "__main__":
    run_analytics()
