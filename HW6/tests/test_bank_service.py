from unittest.mock import patch
from services import bank_service


def test_prepare_bank(sample_valid_bank):
    result = bank_service.prepare_bank(sample_valid_bank)
    assert result == ("CoolBank",)


def test_add_bank_single(sample_valid_bank):
    with patch("services.bank_service.add_objects") as mock_add:
        mock_add.return_value = {"status": "success", "message": "Inserted 1 bank"}

        result = bank_service.add_bank(sample_valid_bank)

        assert result["status"] == "success"
        mock_add.assert_called_once()


def test_add_bank_multiple():
    with patch("services.bank_service.add_objects") as mock_add:
        mock_add.return_value = {"status": "success", "message": "Inserted 2 banks"}

        result = bank_service.add_bank({"name": "Bank A"}, {"name": "Bank B"})

        assert result["status"] == "success"
        mock_add.assert_called_once()


def test_update_bank():
    with patch("services.bank_service.update_object") as mock_update:
        mock_update.return_value = {"status": "success", "message": "Bank updated"}

        result = bank_service.update_bank(1, {"name": "NewBank"})

        assert result["status"] == "success"
        assert "updated" in result["message"].lower()
        mock_update.assert_called_once()


def test_delete_bank():
    with patch("services.bank_service.delete_object") as mock_delete:
        mock_delete.return_value = {"status": "success", "message": "Bank deleted"}

        result = bank_service.delete_bank(1)

        assert result["status"] == "success"
        mock_delete.assert_called_once()


def test_add_bank_from_csv_success():
    with patch("services.bank_service.logger") as mock_logger, \
         patch("services.bank_service.load_csv_to_dicts") as mock_load, \
         patch("services.bank_service.add_bank") as mock_add:

        mock_load.return_value = [{"name": "CSVBank"}]
        mock_add.return_value = {"status": "success", "message": "CSV import succeeded"}

        result = bank_service.add_bank_from_csv("test_path.csv")

        assert result["status"] == "success"
        mock_add.assert_called_once()
        mock_logger.info.assert_called()


def test_add_bank_from_csv_failure():
    with patch("services.bank_service.logger") as mock_logger, \
         patch("services.bank_service.load_csv_to_dicts", side_effect=Exception("CSV error")):

        result = bank_service.add_bank_from_csv("invalid.csv")

        assert result["status"] == "fail"
        assert "failed" in result["message"].lower()
        mock_logger.error.assert_called()
