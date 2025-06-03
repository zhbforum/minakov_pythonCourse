from unittest.mock import patch
from services import bank_service


def test_prepare_bank(sample_valid_bank):
    result = bank_service.prepare_bank(sample_valid_bank)
    assert result == ("CoolBank",)


@patch("services.bank_service.add_objects")
def test_add_bank_single(mock_add_objects, sample_valid_bank):
    mock_add_objects.return_value = {"status": "success", "message": "Inserted 1 bank"}
    result = bank_service.add_bank(sample_valid_bank)
    assert result["status"] == "success"


@patch("services.bank_service.add_objects")
def test_add_bank_multiple(mock_add_objects):
    mock_add_objects.return_value = {"status": "success", "message": "Inserted 2 banks"}
    result = bank_service.add_bank({"name": "Bank A"}, {"name": "Bank B"})
    assert result["status"] == "success"


@patch("services.bank_service.update_object")
def test_update_bank(mock_update_object):
    mock_update_object.return_value = {"status": "success", "message": "Bank updated"}
    result = bank_service.update_bank(1, {"name": "NewBank"})
    assert result["status"] == "success"
    assert "updated" in result["message"].lower()


@patch("services.bank_service.delete_object")
def test_delete_bank(mock_delete_object):
    mock_delete_object.return_value = {"status": "success", "message": "Bank deleted"}
    result = bank_service.delete_bank(1)
    assert result["status"] == "success"


@patch("services.bank_service.load_csv_to_dicts")
@patch("services.bank_service.logger")
@patch("services.bank_service.add_bank")
def test_add_bank_from_csv_success(mock_add_bank, mock_logger, mock_csv_loader):
    mock_csv_loader.return_value = [{"name": "CSVBank"}]
    mock_add_bank.return_value = {"status": "success", "message": "CSV import succeeded"}

    result = bank_service.add_bank_from_csv("test_path.csv")
    assert result["status"] == "success"
    mock_logger.info.assert_called()


@patch("services.bank_service.load_csv_to_dicts", side_effect=Exception("CSV error"))
@patch("services.bank_service.logger")
def test_add_bank_from_csv_failure(mock_logger, mock_csv_loader):
    result = bank_service.add_bank_from_csv("invalid.csv")
    assert result["status"] == "fail"
    assert "failed" in result["message"].lower()
    mock_logger.error.assert_called()
