ALLOWED_ACCOUNT_TYPES = {"credit", "debit"}
ALLOWED_ACCOUNT_STATUSES = {"gold", "silver", "platinum"}
ALLOWED_CURRENCIES = {"USD", "EUR", "GBP", "UAH"}


ACCOUNT_NUMBER_PREFIX = "ID--"
ACCOUNT_NUMBER_LENGTH = 18
ACCOUNT_NUMBER_PATTERN = r"[a-zA-Z]{1,3}-\d+-"  
FULL_NAME_CLEAN_PATTERN = r"[^a-zA-Zа-яА-ЯёЁ\s]"
ACCOUNT_NUMBER_INVALID_CHARS = r"[#%_?&]"
ACCOUNT_NUMBER_REPLACEMENT_CHAR = "-"
ACCOUNT_FIELDS = ["user_id", "type", "account_number", "bank_id", "currency", "amount", "status"]


LOGGER_NAME = "bank_logger"
LOG_FILE_PATH = "logs/banking.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


DEFAULT_ENCODING = "utf-8"
CSV_FOLDER_PATH = "demo"    


CURRENCY_API_URL = "https://api.freecurrencyapi.com/v1/latest"

USER_FIELDS = ["name", "surname", "birth_day", "accounts"]
BANK_FIELDS = ["name"]

LOG_INFO = "info"
LOG_WARN = "warning"
LOG_ERROR = "error"


REQUEST_TIMEOUT = 5