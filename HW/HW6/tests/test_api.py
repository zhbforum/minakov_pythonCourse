from unittest.mock import patch, MagicMock
from api.api import perform_money_transfer


@patch("api.api.transfer_money")
@patch("api.api.db_connection")
def test_perform_money_transfer_success(mock_db_connection, mock_transfer_money):
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = [None, None]
    mock_cursor.fetchone.side_effect = [(1,), (2,)]

    def mock_decorator(func):
        def wrapper():
            return func(cursor=mock_cursor)
        return wrapper

    mock_db_connection.side_effect = mock_decorator
    mock_transfer_money.return_value = {"status": "success", "message": "Transfer completed"}

    result = perform_money_transfer("ID--abc", "ID--xyz", 100.0, "USD")

    assert result["status"] == "success"
    assert "Transfer" in result["message"]
