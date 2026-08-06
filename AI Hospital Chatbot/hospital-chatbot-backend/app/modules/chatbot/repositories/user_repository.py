from typing import Optional
from sqlalchemy.orm import Session
from app.modules.chatbot.repositories.base import CRUDBase
from app.modules.chatbot.models.user import User
from app.modules.chatbot.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserRepository(CRUDBase[User, UserCreate, UserCreate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repo = UserRepository(User)
