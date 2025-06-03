import csv
import os
import requests
from constants import CURRENCY_API_URL, REQUEST_TIMEOUT
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("CURRENCY_API_KEY")


def load_csv_to_dicts(path: str) -> list[dict]:
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    url = f"{CURRENCY_API_URL}?base_currency={from_currency}&currencies={to_currency}"
    headers = {
        "apikey": API_KEY
    }

    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

    if response.status_code == 429 or "limit" in response.text.lower():
        raise RuntimeError("Request limit to currency API exceeded")

    if response.status_code != 200:
        raise RuntimeError(f"Currency API error: {response.status_code} - {response.text}")

    data = response.json()
    rate = data["data"].get(to_currency)
    if not rate:
        raise ValueError(f"Exchange rate for {to_currency} not found.")

    return rate


def normalize_items(*items):
    if len(items) == 1 and isinstance(items[0], list):
        return items[0]
    return list(items)
