import psycopg2
from dotenv import load_dotenv
import os
import argparse


load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

parser = argparse.ArgumentParser(description="Set up the database")
parser.add_argument('--unique-name-surname', action='store_true',
                    help='Add unique constraint to User(name, surname)')
args = parser.parse_args()

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS "Transaction", "Account", "User", "Bank" CASCADE;
""")

cur.execute("""
CREATE TABLE "Bank" (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
""")

cur.execute("""
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    birth_day TEXT,
    accounts TEXT NOT NULL
""" + (",\n    UNIQUE(name, surname)" if args.unique_name_surname else "") + """
);
""")

cur.execute("""
CREATE TABLE "Account" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "User"(id),
    type TEXT CHECK (type IN ('credit', 'debit')) NOT NULL,
    account_number TEXT NOT NULL UNIQUE,
    bank_id INTEGER NOT NULL REFERENCES "Bank"(id),
    currency TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    status TEXT CHECK (status IN ('gold', 'silver', 'platinum'))
);
""")

cur.execute("""
CREATE TABLE "Transaction" (
    id SERIAL PRIMARY KEY,
    bank_sender_name TEXT NOT NULL,
    account_sender_id INTEGER NOT NULL,
    bank_receiver_name TEXT NOT NULL,
    account_receiver_id INTEGER NOT NULL,
    sent_currency TEXT NOT NULL,
    sent_amount NUMERIC NOT NULL,
    datetime TEXT
);
""")

conn.commit()
cur.close()
conn.close()

print("Initial DB setup complete.")