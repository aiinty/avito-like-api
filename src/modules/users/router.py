from fastapi import APIRouter, Depends, status
from src.modules.users.dependencies import get_user_service
from src.modules.users.service import UserService
from src.modules.users.schemas import (
    UserRead,
)
from src.modules.auth.dependencies import get_current_user

users_router = APIRouter(prefix="/user", tags=["User"])

