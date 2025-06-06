from unittest.mock import patch
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


def test_assign_random_discounts_with_users(mock_cursor):
    mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]

    with patch("services.analytics_service.logger") as mock_logger, \
         patch("services.analytics_service.api_response") as mock_response:

        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success" if status else "fail", "message": msg, "data": kwargs.get("data")
        }

        result = assign_random_discounts.__wrapped__(cursor=mock_cursor)

        assert result["status"] == "success"
        assert "Discounts assigned" in result["message"]
        mock_logger.info.assert_called()


def test_get_users_with_debts(mock_cursor):
    mock_cursor.fetchall.return_value = [("Sanya", "Civil")]

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "message": msg, "data": kwargs.get("data")
        }

        result = get_users_with_debts.__wrapped__(cursor=mock_cursor)

        assert "Sanya Civil" in result["data"]
        assert result["status"] == "success"


def test_get_bank_with_biggest_capital(mock_cursor):
    mock_cursor.fetchone.return_value = ("MegaBank", 99999.0)

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "message": msg, "data": kwargs.get("data")
        }

        result = get_bank_with_biggest_capital.__wrapped__(cursor=mock_cursor)

        assert result["data"]["bank"] == "MegaBank"
        assert result["status"] == "success"


def test_get_bank_with_oldest_user(mock_cursor):
    mock_cursor.fetchone.return_value = ("OldBank",)

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "message": msg
        }

        result = get_bank_with_oldest_user.__wrapped__(cursor=mock_cursor)

        assert "OldBank" in result["message"]
        assert result["status"] == "success"


def test_get_bank_with_most_unique_senders(mock_cursor):
    mock_cursor.fetchone.return_value = ("BigBank", 5)

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "message": msg
        }

        result = get_bank_with_most_unique_senders.__wrapped__(cursor=mock_cursor)

        assert "BigBank" in result["message"]
        assert result["status"] == "success"


def test_cleanup_incomplete_data(mock_cursor):
    mock_cursor.rowcount = 2

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "data": kwargs.get("data")
        }

        result = cleanup_incomplete_data.__wrapped__(cursor=mock_cursor)

        assert result["data"]["users_deleted"] == 2
        assert result["data"]["accounts_deleted"] == 2


def test_get_user_transactions_last_3_months_with_data(mock_cursor):
    mock_cursor.fetchall.side_effect = [[(1,), (2,)], [("TX1",), ("TX2",)]]

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "data": kwargs.get("data")
        }

        result = get_user_transactions_last_3_months.__wrapped__(1, cursor=mock_cursor)

        assert len(result["data"]) == 2
        assert result["status"] == "success"


def test_get_currency_transfer_stats(mock_cursor):
    mock_cursor.fetchall.return_value = [("USD", 3), ("EUR", 5)]

    with patch("services.analytics_service.api_response") as mock_response:
        mock_response.side_effect = lambda status, msg, **kwargs: {
            "status": "success", "data": kwargs.get("data")
        }

        result = get_currency_transfer_stats.__wrapped__(cursor=mock_cursor)

        assert result["data"]["USD"] == 3
        assert result["data"]["EUR"] == 5
        assert result["status"] == "success"
