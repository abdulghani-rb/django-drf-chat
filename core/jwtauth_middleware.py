from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from accounts.models import MyUserManager

# from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.backends import TokenBackend

# import jwt
# from core.settings import SECRET_KEY


@database_sync_to_async
def get_user(token):
    try:
        # user = JWTAuthentication().authenticate({'Authorization': f'Bearer {token}'})
        # user = MyUserManager.get_user_by_id(id=1)

        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        # print(valid_data)
        # print(token)
        user_id = valid_data['user_id']
        user = MyUserManager.get_user_by_id(id=user_id)

        # valid_data = jwt.decode(token, SECRET_KEY, algorithms=["HS512"])
        # user_id = valid_data['user_id']
        # user = MyUserManager.get_user_by_id(id=user_id)

        # print(user)
        return user
    except:
        return None

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token = headers[b'authorization'].decode().split(' ')[-1]
            user = await get_user(token)
            if user is not None:
                scope['user'] = user
        return await super().__call__(scope, receive, send)

JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
