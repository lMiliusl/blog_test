import logging
import time
from django.utils import timezone

logger = logging.getLogger('apps')

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Аноним'
        logger.info(f'Запрос: {request.method} {request.path} | Пользователь: {user}')
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.info(f'Ответ: {response.status_code} | Время: {duration:.3f}с')
        
        return response