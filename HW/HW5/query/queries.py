GET_ALL_USER_IDS = """
    SELECT id FROM "User"
"""


CHECK_ACCOUNT_NUMBER_EXISTS = """
    SELECT 1 FROM "Account" WHERE account_number = %s
"""


GET_USERS_WITH_DEBTS = """
    SELECT DISTINCT u.name, u.surname
    FROM "User" u
    JOIN "Account" a ON u.id = a.user_id
    WHERE a.amount < 0
"""


DELETE_INCOMPLETE_USERS = """
    DELETE FROM "User"
    WHERE name IS NULL OR name = ''
       OR surname IS NULL OR surname = ''
       OR accounts IS NULL OR accounts = ''
"""


GET_BANK_WITH_BIGGEST_CAPITAL = """
    SELECT b.name, SUM(a.amount) as total_capital
    FROM "Bank" b
    JOIN "Account" a ON b.id = a.bank_id
    GROUP BY b.name
    ORDER BY total_capital DESC
    LIMIT 1
"""


GET_OLDEST_USER_BANK = """
    SELECT b.name
    FROM "User" u
    JOIN "Account" a ON u.id = a.user_id
    JOIN "Bank" b ON a.bank_id = b.id
    WHERE u.birth_day IS NOT NULL
    ORDER BY u.birth_day ASC
    LIMIT 1
"""


GET_MOST_UNIQUE_SENDERS_BANK = """
    SELECT b.name, COUNT(DISTINCT a.user_id) as user_count
    FROM "Transaction" t
    JOIN "Account" a ON t.account_sender_id = a.id
    JOIN "Bank" b ON a.bank_id = b.id
    GROUP BY b.name
    ORDER BY user_count DESC
    LIMIT 1
"""


GET_ACCOUNT_IDS_BY_USER_ID = """
    SELECT id FROM "Account"
    WHERE user_id = %s
"""


DELETE_INCOMPLETE_ACCOUNTS = """
    DELETE FROM "Account"
    WHERE user_id IS NULL
       OR type IS NULL OR type = ''
       OR account_number IS NULL OR account_number = ''
       OR bank_id IS NULL
       OR currency IS NULL OR currency = ''
       OR amount IS NULL
"""


GET_LAST_3_MONTH_TRANSACTIONS = """
    SELECT *
    FROM "Transaction"
    WHERE account_sender_id = ANY(%s)
      AND datetime >= %s
"""


GET_CURRENCY_STATS = """
    SELECT sent_currency, COUNT(*) as transfer_count
    FROM "Transaction"
    GROUP BY sent_currency
    ORDER BY transfer_count DESC
"""


GET_ACCOUNT_BY_ID = """
    SELECT id, amount, currency, bank_id FROM "Account"
    WHERE id = %s
"""


UPDATE_ACCOUNT_BALANCE = """
    UPDATE "Account" SET amount = amount + %s WHERE id = %s
"""


GET_BANK_NAME_BY_ID = """
    SELECT name FROM "Bank" WHERE id = %s
"""


INSERT_TRANSACTION = """
    INSERT INTO "Transaction" (
        bank_sender_name, account_sender_id,
        bank_receiver_name, account_receiver_id,
        sent_currency, sent_amount, datetime
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
