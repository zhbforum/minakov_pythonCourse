from unittest.mock import patch
from services.generic_service import (
    update_info,
    delete_info,
    add_objects,
    update_object,
    delete_object,
)


def test_update_info_success(mock_cursor):
    mock_cursor.rowcount = 1  

    with patch("services.generic_service.api_response") as mock_resp:
        mock_resp.side_effect = lambda status, msg, **kwargs: {
            "status": "success" if status else "fail",
            "message": msg
        }

        result = update_info.__wrapped__("users", "id", 1, {"name": "New Name"}, cursor=mock_cursor)

        assert result["status"] == "success"
        assert "Updated" in result["message"]
        mock_resp.assert_called_once()


def test_update_info_no_fields(mock_cursor):
    result = update_info.__wrapped__("users", "id", 1, {}, cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "No fields" in result["message"]


def test_delete_info_success(mock_cursor):
    with patch("services.generic_service.api_response") as mock_resp:
        mock_resp.side_effect = lambda status, msg, **kwargs: {
            "status": "success" if status else "fail",
            "message": msg
        }

        result = delete_info.__wrapped__("accounts", {"id": 1, "user_id": 3}, cursor=mock_cursor)

        assert result["status"] == "success"
        assert "deleted" in result["message"]
        mock_resp.assert_called_once()


def test_delete_info_no_criteria(mock_cursor):
    result = delete_info.__wrapped__("accounts", {}, cursor=mock_cursor)

    assert result["status"] == "fail"
    assert "No criteria" in result["message"]


def test_add_objects_partial_success(mock_cursor):
    mock_cursor.fetchone.side_effect = [(1,), (3,)]
    mock_cursor.execute.side_effect = [None, Exception("fail"), None]

    result = add_objects(
        cursor=mock_cursor,
        table="banks",
        fields=["name", "country"],
        prepared_items=[
            ("Bank A", "DE"),
            ("Broken Bank", "XX"),
            ("Bank C", "US"),
        ],
        entity_name="bank",
    )

    assert result["status"] == "success"
    assert "Inserted 2 bank(s), skipped 1" in result["message"]
    assert len(result["data"]) == 2


def test_update_object_success():
    with patch("services.generic_service.update_info") as mock_update_info:
        mock_update_info.return_value = {"status": "success", "message": "OK"}

        result = update_object("banks", 1, {"country": "DE"})

        assert result["status"] == "success"
        mock_update_info.assert_called_once()


def test_delete_object_success():
    with patch("services.generic_service.delete_info") as mock_delete_info:
        mock_delete_info.return_value = {"status": "success", "message": "Deleted"}

        result = delete_object("accounts", 2)

        assert result["status"] == "success"
        mock_delete_info.assert_called_once()
