import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_cursor():
    mock = MagicMock()
    mock.rowcount = 2
    return mock


@pytest.fixture
def sample_valid_account():
    return {
        "user_id": 1,
        "bank_id": 2,
        "type": "checking",
        "account_number": "ID--acc-999",
        "currency": "USD",
        "amount": 100.0,
        "status": "active"
    }


@pytest.fixture
def sample_valid_user():
    return {
        "user_full_name": "John Doe",
        "birth_day": "1990-01-01",
        "accounts": "111,222"
    }
    
    
@pytest.fixture
def sample_users():
    return [
        {"user_full_name": "Sasha legenda", "birth_day": "2001-05-12", "accounts": "321"},
        {"user_full_name": "Sasha molodec", "birth_day": "1995-03-20", "accounts": "999,000"}
    ]
   

@pytest.fixture
def sample_valid_bank():
    return {
        "name": "CoolBank"
    }


@pytest.fixture
def mock_api_response_success():
    return lambda status, msg, **kwargs: {
        "status": "success", "message": msg, "data": kwargs.get("data")
    }

@pytest.fixture
def mock_api_response_fail():
    return lambda status, msg, **kwargs: {
        "status": "fail", "message": msg, "data": kwargs.get("data")
    }


@pytest.fixture
def mock_db_wrapper(mock_cursor):
    def _wrap(func):
        return lambda *args, **kwargs: func(cursor=mock_cursor, *args, **kwargs)
    return _wrap
