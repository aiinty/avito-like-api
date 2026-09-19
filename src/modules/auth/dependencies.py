from fastapi import Depends
from src.modules.auth.service import AuthService
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService


def get_auth_service(user_service: UserService = Depends(get_user_service)):
    return AuthService(user_service)
