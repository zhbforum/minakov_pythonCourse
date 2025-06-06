import pytest
from utils.utils import normalize_items, load_csv_to_dicts, get_exchange_rate
from utils.response_utils import api_response
from unittest.mock import patch


def test_normalize_items_single_list():
    input_data = [{"a": 1}, {"b": 2}]
    assert normalize_items(input_data) == input_data


def test_normalize_items_variadic():
    assert normalize_items({"a": 1}, {"b": 2}) == [{"a": 1}, {"b": 2}]


def test_normalize_items_empty():
    assert normalize_items() == []


def test_load_csv_to_dicts(tmp_path):
    csv_file = tmp_path / "temp.csv"
    csv_file.write_text("name,age\nVadim,30\nDenis,25", encoding="utf-8")

    data = load_csv_to_dicts(str(csv_file))
    assert data == [
        {"name": "Vadim", "age": "30"},
        {"name": "Denis", "age": "25"}
    ]


def test_get_exchange_rate_success():
    with patch("utils.utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {"EUR": 0.91}
        }

        rate = get_exchange_rate("USD", "EUR")

        assert rate == 0.91
        mock_get.assert_called_once()


def test_get_exchange_rate_no_rate():
    with patch("utils.utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {}
        }

        with pytest.raises(ValueError, match="not found"):
            get_exchange_rate("USD", "ZHB")

        mock_get.assert_called_once()


def test_get_exchange_rate_api_error():
    with patch("utils.utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Server Error"

        with pytest.raises(RuntimeError, match="500"):
            get_exchange_rate("USD", "EUR")

        mock_get.assert_called_once()


def test_get_exchange_rate_limit_exceeded():
    with patch("utils.utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 429
        mock_get.return_value.text = "Rate limit exceeded"

        with pytest.raises(RuntimeError, match="limit.*exceeded"):
            get_exchange_rate("USD", "EUR")

        mock_get.assert_called_once()


def test_api_response_success():
    result = api_response(True, "All good", data={"key": "value"})

    assert result["status"] == "success"
    assert result["message"] == "All good"
    assert result["data"] == {"key": "value"}


def test_api_response_fail_with_log(caplog):
    with caplog.at_level("INFO"):
        result = api_response(False, "Something failed", log_type="info")

        assert result["status"] == "fail"
        assert "Something failed" in result["message"]
        assert "Something failed" in caplog.text
