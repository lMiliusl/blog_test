from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from apps.users.api import router as user_router
import json

api = NinjaAPI(
    title='Blog API',
    description='API для блога',
    version='1.0.0'
)

api.add_router('/users/', user_router)