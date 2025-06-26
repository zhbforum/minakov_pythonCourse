from logger import logger


def api_response(success: bool, message: str, data=None, log_type: str = None) -> dict:
    
    if log_type:   
        log_func = getattr(logger, log_type, logger.info)
        log_func(message)

    return {
        "status": "success" if success else "fail",
        "message": message,
        "data": data
    }
    