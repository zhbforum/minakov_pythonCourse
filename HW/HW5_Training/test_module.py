import module
from unittest.mock import Mock, patch


def test_add_numbers():
    assert module.add_numbers(3, 4) == 7
    assert module.add_numbers(-1, 1) == 0
    

def test_is_even():
    assert module.is_even(2) is True
    assert module.is_even(3) is False
    assert module.is_even(0) is True
    assert module.is_even(-2) is True
    assert module.is_even(-3) is False
    

@patch("module.requests.get")
def test_fetch_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"key": "value"}
    result = module.fetch_data("http://example.com")
    assert result == {"key": "value"}
    

@patch("module.requests.get")
def test_fetch_data_fail(mock_get):
    mock_get.return_value.status_code = 404
    result = module.fetch_data("http://example.com")
    assert result is None
    

def test_process_mock_object_positive():
    mock_obj = Mock()
    mock_obj.value = 5
    assert module.process_mock_object(mock_obj) == 10
    

def test_process_mock_object_negative():
    mock_obj = Mock()
    mock_obj.value = -5
    assert module.process_mock_object(mock_obj) is None
    

def test_divide_numbers_success():
    assert module.divide_numbers(10, 2) == 5.0


def test_divide_numbers_zero_division(capfd):
    module.divide_numbers(1, 0)
    out, _ = capfd.readouterr()
    assert "Cannot divide by zero" in out


def test_divide_numbers_type_error(capfd):
    module.divide_numbers("a", 2)
    out, _ = capfd.readouterr()
    assert "Unsupported operand type" in out


@patch("module.requests.get")
def test_check_even_odd(mock_get):
    mock_get.side_effect = [
        Mock(json=Mock(return_value={"results": [{"value": 1}]})),
        Mock(json=Mock(return_value={"results": [{"value": 2}]})),
        Mock(json=Mock(return_value={"results": [{"value": 3}]})),
    ]
    result = module.check_even_odd([1, 2, 3], "http://example.com")
    assert result == ["Odd", "Even", "Odd"]


def test_data_processor():
    processor = module.DataProcessor()
    data = [1, 2, 3]
    assert processor.process_data(data) == [2, 4, 6]
    assert processor.analyze_data(data) == 12


def test_run_data_pipeline():
    mock_processor = Mock()
    mock_result = Mock()
    mock_processor.process_data.return_value.analyze_data.return_value = mock_result
    module.run_data_pipeline(mock_processor)
    mock_result.save_result.assert_called_once()

