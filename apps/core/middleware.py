import logging
import time
from django.utils import timezone

logger = logging.getLogger('apps')

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        try:
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                user = request.user.username
            else:
                user = 'Аноним'
        except:
            user = 'Аноним (ошибка получения)'

        logger.info(f'Запрос: {request.method} {request.path} | Пользователь: {user}')

        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f'Ошибка при обработке запроса: {str(e)}')
            raise
    
        duration = time.time() - start_time
        
        logger.info(f"Ответ: {response.status_code if hasattr(response, 'status_code') else '???'} | Время: {duration:.3f}с")
        
        return response