import logging
from functools import wraps

logger = logging.getLogger(__name__)


def log_api_view(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        logger.info(f'View function {view_func.__name__} was called from {view_func.__module__}')
        try:
            response = view_func(*args, **kwargs)
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(
                    f"View function {view_func.__name__} returned successful response with status code: {response.status_code}")
            elif response.status_code >= 400 and response.status_code < 500:
                logger.warning(
                    f"View function {view_func.__name__} returned client error response with status code: {response.status_code}")
            elif response.status_code >= 500:
                logger.error(
                    f"View function {view_func.__name__} returned server error response with status code: {response.status_code}")
            else:
                logger.info(
                    f"View function {view_func.__name__} returned response with status code: {response.status_code}")
        except Exception as e:
            logger.exception(f"View function {view_func.__name__} raised an exception: {str(e)}")
            raise
        logger.debug(f"View function {view_func.__name__} response data: {response.data}")
        return response
    return wrapper


def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Function {func.__name__} was called from {func.__module__}')
        try:
            result = func(*args, **kwargs)
            logger.info(f'Function {func.__name__} executed successfully')
        except Exception as e:
            logger.exception(f'Function {func.__name__} raised and exception: {str(e)}')
            raise
        return result
    return wrapper
