import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.modules.chatbot.models.user import User
from app.modules.chatbot.repositories.user_repository import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(db: Session = Depends(get_db)) -> User:
    user = user_repo.get_by_email(db, email="demo_user@hospital.local")
    if not user:
        from app.modules.chatbot.schemas.user import UserCreate
        user = user_repo.create(db, obj_in=UserCreate(username="demo_user", email="demo_user@hospital.local", password="mockpassword"))
    return user
