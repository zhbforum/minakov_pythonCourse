from unittest.mock import patch
from services.account_service import add_account, update_account, delete_account, add_account_from_csv


def test_add_account_success(mock_cursor, sample_valid_account):
    mock_cursor.fetchall.return_value = [("ID--acc-123",)]

    with patch("services.account_service.add_objects") as mock_add:
        mock_add.return_value = {"status": "success", "message": "1 account(s) added"}

        result = add_account.__wrapped__(sample_valid_account, cursor=mock_cursor)

        assert result["status"] == "success"
        assert "added" in result["message"]


def test_update_account_valid():
    with patch("services.account_service.update_object") as mock_update:
        mock_update.return_value = {"status": "success", "message": "Account updated"}

        result = update_account(1, {
            "type": "credit",
            "currency": "EUR",
            "account_number": "ID--acc-321-000001"
        })

        assert result["status"] == "success"
        assert "updated" in result["message"]


def test_delete_account():
    with patch("services.account_service.delete_object") as mock_delete:
        mock_delete.return_value = {"status": "success", "message": "Account deleted"}

        result = delete_account(123)

        assert result["status"] == "success"
        assert "deleted" in result["message"]


def test_add_account_from_csv_success():
    with patch("services.account_service.logger") as mock_logger, \
         patch("services.account_service.load_csv_to_dicts") as mock_load, \
         patch("services.account_service.add_account") as mock_add:

        mock_load.return_value = [{
            "user_id": 1,
            "bank_id": 1,
            "type": "checking",
            "account_number": "acc123",
            "currency": "USD",
            "amount": 100.0
        }]
        mock_add.return_value = {"status": "success", "message": "Imported"}

        result = add_account_from_csv("test.csv")

        assert result["status"] == "success"
        assert "imported" in result["message"].lower()
        mock_logger.info.assert_called()
