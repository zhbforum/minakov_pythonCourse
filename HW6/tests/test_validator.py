import pytest
from validator import (
    validate_account_type,
    validate_account_status,
    validate_currency,
    validate_account_number,
    validate_full_name
)


def test_validate_account_type_valid():
    validate_account_type("credit")
    validate_account_type("debit")


@pytest.mark.parametrize("account_type", ["saving", "investment", "", None])
def test_validate_account_type_invalid(account_type):
    with pytest.raises(ValueError):
        validate_account_type(account_type)


def test_validate_account_status_valid():
    validate_account_status("gold")
    validate_account_status("silver")
    validate_account_status("platinum")


@pytest.mark.parametrize("status", ["basic", "premium", "", None])
def test_validate_account_status_invalid(status):
    with pytest.raises(ValueError):
        validate_account_status(status)


def test_validate_currency_valid():
    validate_currency("USD")
    validate_currency("EUR")
    validate_currency("GBP")
    validate_currency("UAH")


@pytest.mark.parametrize("currency", ["CZH", "BTC", "", None])
def test_validate_currency_invalid(currency):
    with pytest.raises(ValueError):
        validate_currency(currency)


@pytest.mark.parametrize("number", [
    "ID--abc-1234567-xz",
    "ID--xyx-2345678-xx"
])
def test_validate_account_number_valid(number):
    assert validate_account_number(number) == number


@pytest.mark.parametrize("number", [
    "abc-1234567-xz",                 
    "ID--ab-12-xz",                    
    "ID--abc-1234567-xz#",             
    "ID--wrongformat",                 
    "ID--ab_1234567?xz",               
])
def test_validate_account_number_invalid(number):
    with pytest.raises(ValueError):
        validate_account_number(number)


def test_validate_full_name_valid():
    assert validate_full_name("John Doe") == ("John", "Doe")
    assert validate_full_name("  Oleg! #Ananko ") == ("Oleg", "Ananko")


@pytest.mark.parametrize("full_name", ["", "Alex", "    ", "!!!"])
def test_validate_full_name_invalid(full_name):
    with pytest.raises(ValueError):
        validate_full_name(full_name)
