from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class TokenAuth(HttpBearer):
    def authentficate (sefl, request, token):
        try:
            user = User.objects.get(token=token)
            request.user = user
            return user
        except User.DoesNotExist:
            return None
        
token_auth = TokenAuth()