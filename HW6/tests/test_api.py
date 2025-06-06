from unittest.mock import patch
from api.api import perform_money_transfer


def test_perform_money_transfer_success(mock_cursor):
    mock_cursor.execute.side_effect = [None, None]
    mock_cursor.fetchone.side_effect = [(1,), (2,)]

    def mock_decorator(func):
        def wrapper(*args, **kwargs):
            return func(cursor=mock_cursor, *args, **kwargs)
        return wrapper

    with patch("api.api.db_connection", side_effect=mock_decorator), \
         patch("api.api.transfer_money") as mock_transfer:

        mock_transfer.return_value = {"status": "success", "message": "Transfer completed"}

        result = perform_money_transfer("ID--abc", "ID--xyz", 100.0, "USD")

        assert result["status"] == "success"
        assert "Transfer" in result["message"]
        mock_transfer.assert_called_once()
