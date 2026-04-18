from app.domain.repositories import IUserRepository
from app.domain.entities import User, Email
from app.infrastructure.orm_models import UserModel
from app.db import db

class SqlAlchemyUserRepository(IUserRepository):
    def save(self, user: User) -> None:
        
        orm_user = UserModel(
            email=user.email.value, 
            password=user.password_hash
        )
        
        db.session.add(orm_user)
        db.session.commit()
        
        user.user_id = orm_user.user_id

    def get_by_email(self, email: Email) -> User | None:

        orm_user = UserModel.query.filter_by(email=email.value).first()
        
        if orm_user is None:
            return None
            
        return User(
            user_id=orm_user.user_id,
            email=Email(orm_user.email),
            password_hash=orm_user.password
        )