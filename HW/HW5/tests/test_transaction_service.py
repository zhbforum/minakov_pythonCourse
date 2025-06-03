from unittest.mock import patch
from services.transaction_service import transfer_money_logic


def make_account(id, balance, currency, bank_id):
    return (id, balance, currency, bank_id)


@patch("services.transaction_service.get_account_by_id")
@patch("services.transaction_service.get_exchange_rate")
@patch("services.transaction_service.get_bank_name_by_id")
def test_successful_transfer(mock_get_bank_name, mock_get_rate, mock_get_account, mock_cursor):
    sender = make_account(1, 100.0, "USD", 10)
    receiver = make_account(2, 50.0, "USD", 20)

    mock_get_account.side_effect = [sender, receiver]
    mock_get_rate.return_value = 1.0
    mock_get_bank_name.side_effect = ["BankA", "BankB"]

    result = transfer_money_logic(1, 2, 25.0, "USD", cursor=mock_cursor)

    assert result["status"] == "success"
    assert "sent successfully" in result["message"]
    assert mock_cursor.execute.call_count == 3


@patch("services.transaction_service.get_account_by_id")
def test_transfer_insufficient_funds(mock_get_account, mock_cursor):
    sender = make_account(1, 10.0, "USD", 10)
    receiver = make_account(2, 100.0, "USD", 20)
    mock_get_account.side_effect = [sender, receiver]

    result = transfer_money_logic(1, 2, 50.0, "USD", cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "Insufficient balance" in result["message"]


@patch("services.transaction_service.get_account_by_id")
def test_transfer_account_not_found(mock_get_account, mock_cursor):
    mock_get_account.side_effect = [None, None]

    result = transfer_money_logic(1, 2, 50.0, "USD", cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "not found" in result["message"]


@patch("services.transaction_service.get_account_by_id")
@patch("services.transaction_service.get_exchange_rate")
@patch("services.transaction_service.get_bank_name_by_id")
def test_transfer_with_conversion(mock_get_bank_name, mock_get_rate, mock_get_account, mock_cursor):
    sender = make_account(1, 100.0, "USD", 10)
    receiver = make_account(2, 50.0, "EUR", 20)

    mock_get_account.side_effect = [sender, receiver]
    mock_get_rate.return_value = 0.9
    mock_get_bank_name.side_effect = ["BankA", "BankB"]

    result = transfer_money_logic(1, 2, 20.0, "USD", cursor=mock_cursor)

    assert result["status"] == "success"
    mock_get_rate.assert_called_once_with("USD", "EUR")


@patch("services.transaction_service.get_account_by_id")
def test_transfer_to_self(mock_get_account, mock_cursor):
    acc = make_account(1, 100.0, "USD", 10)
    mock_get_account.side_effect = [acc, acc]

    result = transfer_money_logic(1, 1, 10.0, "USD", cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "same account" in result["message"].lower()


@patch("services.transaction_service.get_account_by_id")
def test_transfer_zero_amount(mock_get_account, mock_cursor):
    sender = make_account(1, 100.0, "USD", 10)
    receiver = make_account(2, 50.0, "USD", 20)
    mock_get_account.side_effect = [sender, receiver]

    result = transfer_money_logic(1, 2, 0.0, "USD", cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "greater than zero" in result["message"].lower()


@patch("services.transaction_service.get_account_by_id")
@patch("services.transaction_service.get_exchange_rate")
def test_exchange_rate_fetch_fail(mock_get_rate, mock_get_account, mock_cursor):
    sender = make_account(1, 100.0, "USD", 10)
    receiver = make_account(2, 50.0, "EUR", 20)
    mock_get_account.side_effect = [sender, receiver]

    mock_get_rate.side_effect = Exception("Exchange rate error")

    result = transfer_money_logic(1, 2, 15.0, "USD", cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "conversion error" in result["message"].lower()
