from unittest.mock import patch, MagicMock
from services.analytics_service import (
    assign_random_discounts,
    get_users_with_debts,
    get_bank_with_biggest_capital,
    get_bank_with_oldest_user,
    get_bank_with_most_unique_senders,
    cleanup_incomplete_data,
    get_user_transactions_last_3_months,
    get_currency_transfer_stats
)

def mock_db(func, cursor_return):
    def wrapper(*args, **kwargs):
        return func(cursor=cursor_return, *args, **kwargs)
    return wrapper


@patch("services.analytics_service.logger")
@patch("services.analytics_service.api_response")
def test_assign_random_discounts_with_users(mock_response, mock_logger):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success" if status else "fail", "message": msg, "data": kwargs.get("data")
    }

    result = mock_db(assign_random_discounts.__wrapped__, mock_cursor)()
    assert result["status"] == "success"
    assert "Discounts assigned" in result["message"]


@patch("services.analytics_service.api_response")
def test_get_users_with_debts(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Sanya", "Civil")]

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "message": msg, "data": kwargs.get("data")
    }

    result = mock_db(get_users_with_debts.__wrapped__, mock_cursor)()
    assert "Sanya Civil" in result["data"]
    assert result["status"] == "success"


@patch("services.analytics_service.api_response")
def test_get_bank_with_biggest_capital(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("MegaBank", 99999.0)

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "message": msg, "data": kwargs.get("data")
    }

    result = mock_db(get_bank_with_biggest_capital.__wrapped__, mock_cursor)()
    assert result["data"]["bank"] == "MegaBank"


@patch("services.analytics_service.api_response")
def test_get_bank_with_oldest_user(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("OldBank",)

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "message": msg
    }

    result = mock_db(get_bank_with_oldest_user.__wrapped__, mock_cursor)()
    assert "OldBank" in result["message"]


@patch("services.analytics_service.api_response")
def test_get_bank_with_most_unique_senders(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("BigBank", 5)

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "message": msg
    }

    result = mock_db(get_bank_with_most_unique_senders.__wrapped__, mock_cursor)()
    assert "BigBank" in result["message"]


@patch("services.analytics_service.api_response")
def test_cleanup_incomplete_data(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 2

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "data": kwargs.get("data")
    }

    result = mock_db(cleanup_incomplete_data.__wrapped__, mock_cursor)()
    assert result["data"]["users_deleted"] == 2
    assert result["data"]["accounts_deleted"] == 2


@patch("services.analytics_service.api_response")
def test_get_user_transactions_last_3_months_with_data(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [[(1,), (2,)], [("TX1",), ("TX2",)]]

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "data": kwargs.get("data")
    }

    result = mock_db(get_user_transactions_last_3_months.__wrapped__, mock_cursor)(1)
    assert len(result["data"]) == 2


@patch("services.analytics_service.api_response")
def test_get_currency_transfer_stats(mock_response):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("USD", 3), ("EUR", 5)]

    mock_response.side_effect = lambda status, msg, **kwargs: {
        "status": "success", "data": kwargs.get("data")
    }

    result = mock_db(get_currency_transfer_stats.__wrapped__, mock_cursor)()
    assert result["data"]["USD"] == 3
