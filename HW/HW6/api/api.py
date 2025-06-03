from services.transaction_service import transfer_money
from db import db_connection


def perform_money_transfer(
    sender_account_number: str,
    receiver_account_number: str,
    amount: float,
    currency: str
) -> dict:
    @db_connection
    def run_transfer(cursor=None):
        cursor.execute('SELECT id FROM "Account" WHERE account_number = %s', (sender_account_number,))
        sender = cursor.fetchone()

        cursor.execute('SELECT id FROM "Account" WHERE account_number = %s', (receiver_account_number,))
        receiver = cursor.fetchone()

        if not sender or not receiver:
            return {"status": "fail", "message": "Sender or receiver account number not found."}

        return transfer_money(
            sender_account_id=sender[0],
            receiver_account_id=receiver[0],
            amount=amount,
            currency=currency
        )

    return run_transfer()
