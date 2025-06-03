import pytest
from unittest.mock import patch
from services.user_service import add_user, update_user, delete_user, add_user_from_csv


def test_add_user_valid_single(sample_valid_user):
    with patch("services.user_service.add_objects") as mock_add:
        mock_add.return_value = {"status": "success", "message": "Inserted 1 user(s)", "data": [1]}

        result = add_user(sample_valid_user)

        assert result["status"] == "success"
        assert result["data"] == [1]
        mock_add.assert_called_once()


def test_add_user_valid_list(sample_users):
    with patch("services.user_service.add_objects") as mock_add:
        mock_add.return_value = {"status": "success", "message": "2 inserted", "data": [1, 2]}

        result = add_user(sample_users)

        assert result["status"] == "success"
        assert len(result["data"]) == 2


def test_add_user_invalid_name():
    user = {"user_full_name": "Bareksten", "accounts": "777"}
    with patch("services.user_service.add_objects") as mock_add:
        result = add_user(None, user)
        assert result["status"] == "fail"
        assert "Full name" in result["message"]
        mock_add.assert_not_called()


def test_add_user_missing_accounts():
    user = {"user_full_name": "Jack Daniels"}

    with patch("services.user_service.add_objects") as mock_add:
        result = add_user(None, user)

        assert result["status"] == "fail"
        assert "accounts" in result["message"]


def test_update_user_valid_partial():
    with patch("services.user_service.update_object") as mock_update:
        mock_update.return_value = {"status": "success", "message": "Updated"}

        result = update_user(1, {"birth_day": "2002-01-01"})

        assert result["status"] == "success"
        mock_update.assert_called_once()


def test_update_user_full_name():
    with patch("services.user_service.update_object") as mock_update:
        mock_update.return_value = {"status": "success", "message": "Updated"}

        result = update_user(3, {"user_full_name": "Kakoeto Imya"})

        assert result["status"] == "success"
        mock_update.assert_called_once()


def test_update_user_invalid_name():
    with pytest.raises(ValueError, match="Full name"):
        update_user(2, {"user_full_name": "Wrong"})


def test_update_user_ignored_fields():
    result = update_user(4, {"not_a_field": "value"})

    assert result["status"] == "fail"
    assert "No fields provided" in result["message"]


def test_delete_user_valid():
    with patch("services.user_service.delete_object") as mock_delete:
        mock_delete.return_value = {"status": "success", "message": "Deleted"}

        result = delete_user(99)

        assert result["status"] == "success"
        mock_delete.assert_called_once()


def test_add_user_from_csv_success(tmp_path):
    csv = tmp_path / "valid.csv"
    csv.write_text("user_full_name,birth_day,accounts\nVanka Vstanka,1991-11-11,1234", encoding="utf-8")

    with patch("services.user_service.add_user") as mock_add:
        mock_add.return_value = {"status": "success", "message": "Inserted"}

        result = add_user_from_csv(str(csv))

        assert result["status"] == "success"
        mock_add.assert_called_once()


def test_add_user_from_csv_invalid_path():
    result = add_user_from_csv("nonexistent.csv")

    assert result["status"] == "fail"
    assert "failed" in result["message"].lower()
