import logging
from functools import wraps

logger = logging.getLogger('apps')

def log_crud_operations(model_name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            operation = func.__name__
            logger.info(f'CRUD операция: {model_name} - {operation} - Пользователь: {request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Аноним'}')
            result = func(request, *args, **kwargs)

            if hasattr(result, 'status_code'):
                if 200 <= result.status_code < 300:
                    logger.info(f'CRUD выполнен: {model_name} - {operation} - Статус: {result.status_code}')
                else:
                    logger.info(f'CRUD ошибка: {model_name} - {operation} - Статус: {result.status_code}')
            
            return result
        return wrapper
    return decorator