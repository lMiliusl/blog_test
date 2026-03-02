import logging
from ninja import Router
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User
from .schemas import UserRegisterSchema, UserLoginSchema, UserOutSchema, TokenSchema
from .auth import token_auth
from datetime import datetime

logger = logging.getLogger('apps')
router = Router(tags=['users'])

@router.post('/register', response=TokenSchema)
def register(request, data: UserRegisterSchema):
    
    logger.info(f'Попытка регистрации нового пользователя: {data.username}')

    if User.objects.filter(username=data.username).exists():
        
        logger.warning(f'Регистрация не выполнена: пользователь {data.username} уже существует')

        return 400, {'error': 'Пользователь с таким именем уже существует.'}
    
    user = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email or '',
        first_name=data.first_name,
        last_name=data.last_name
    )

    token = user.generate_token()
    user.refresh_from_db()
    logger.info(f'Успешная регистрация пользователя: {data.username} (ID: {user.id})')

    return{
        'token': token,
        'user': user
    }

@router.post('/login', response=TokenSchema)
def login(request, data: UserLoginSchema):

    logger.info(f'Попытка авторизации пользователя: {data.username}')

    user = authenticate(
        username=data.username,
        password=data.password
    )

    if user is None:
        logger.warning(f'Пользователь {data.username} не авторизован')
        return 401, {'error': 'Неверное имя пользователя или пароль'}
    
    if not user.token:
        token = user.generate_token()
    else:
        token = user.token
    logger.info(f'Успешная авторизация пользователя: {data.username} (ID: {user.id})')
    
    return {
        'token': token,
        'user': user
    }

@router.get('/me', response=UserOutSchema, auth=token_auth)
def get_current_user(request):
    return request.user

@router.post('/logout', auth=token_auth)
def logout(request):
    user = request.user
    logger.info(f'Выход пользователя: {user.username} (ID: {user.id})')
    user.token = None
    user.save()
    return {'success': True}