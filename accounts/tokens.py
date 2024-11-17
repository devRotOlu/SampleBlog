# this file is implemented in order to allow for
# manual tokens generation.

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

"""
get_user_model is a method that returns the current active user model:
If a custom user model is specified, it returns that model
Otherwise, it returns User
"""
User = get_user_model()

def create_jwt_pair_for_user(user:User):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access":str(refresh.access_token),
        "refresh":str(refresh)
    }

    return tokens