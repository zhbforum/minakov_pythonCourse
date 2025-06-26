from api import (
    add_users_from_csv,
    add_banks_from_csv,
    add_accounts_from_csv,
    perform_money_transfer
)

if __name__ == "__main__":
    print(add_banks_from_csv("demo/banks.csv"))
    print(add_users_from_csv("demo/users.csv"))
    print(add_accounts_from_csv("demo/accounts.csv"))
    
    result = perform_money_transfer(
        sender_account_number="ID--abc-1234567-xz",
        receiver_account_number="ID--xyz-9876543-ab",
        amount=25.75,
        currency="USD"
    )
    print(result)
