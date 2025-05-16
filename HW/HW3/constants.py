# API settings
BASE_URL = "https://randomuser.me/api/"
CSV_FORMAT = "csv"
MAX_ROWS = 5000

# Date formats
DATE_FMT_DOB = "%m/%d/%Y"
DATE_FMT_REG = "%m-%d-%Y, %H:%M:%S"
DATE_FMT_CURRENT = "%Y-%m-%d %H:%M:%S %z"
ERROR_INVALID_DOB = "Invalid DOB date format '{}': {}"

# Timezone settings
DEFAULT_TIMEZONE = "UTC"
ERROR_INVALID_TIMEZONE = "Couldn't parse timezone offset '{}': {}"

# Mapping by title 
TITLE_MAP = {
    "Mrs": "missis",
    "Ms": "miss",
    "Mr": "mister",
    "Madame": "mademoiselle"
}

# Logging 
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_LOG_FILE = "script.log"

# Archive settings
ARCHIVE_EXTENSION = ".zip"
