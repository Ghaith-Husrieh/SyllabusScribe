import logging
from functools import partial, wraps

logger = logging.getLogger(__name__)


def log_api_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_info = f"User:({user.username}({user.id}))" if user.is_authenticated else "User:Anonymous User"
        logger.info(
            f'{user_info} | View function {view_func.__name__} was called from {view_func.__module__} | Method:{request.method} | Path:{request.path}'
        )
        try:
            response = view_func(request, *args, **kwargs)
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(
                    f"{user_info} | View function {view_func.__name__} returned successful response with status code: {response.status_code}")
            elif response.status_code >= 400 and response.status_code < 500:
                logger.warning(
                    f"{user_info} | View function {view_func.__name__} returned client error response with status code: {response.status_code}")
            elif response.status_code >= 500:
                logger.error(
                    f"{user_info} | View function {view_func.__name__} returned server error response with status code: {response.status_code}")
            else:
                logger.info(
                    f"{user_info} | View function {view_func.__name__} returned response with status code: {response.status_code}")
        except Exception as e:
            logger.exception(
                f"{user_info} | View function {view_func.__name__} raised an exception: {str(e)}")
            raise
        logger.debug(
            f"{user_info} | View function {view_func.__name__} response data: {response.data}")
        return response
    return wrapper


def log_function(func=None, log_result=True):
    if func == None:
        return partial(log_function, log_result=log_result)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Function {func.__name__} was called from {func.__module__}')
        try:
            result = func(*args, **kwargs)
            if log_result == True:
                logger.info(f'Function {func.__name__} finished execution | RESULT:{result}')
            else:
                logger.info(f'Function {func.__name__} finished execution')
        except Exception as e:
            logger.exception(f'Function {func.__name__} raised and exception: {str(e)}')
            raise
        return result
    return wrapper
