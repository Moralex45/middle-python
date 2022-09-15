import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import Column, VARCHAR, ForeignKey, TEXT, TIMESTAMP, BOOLEAN
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(VARCHAR(255), nullable=False, unique=True)
    pwd_hash = Column(VARCHAR(255))
    is_superuser = Column(BOOLEAN(), default=False)
    data_joined = Column(TIMESTAMP(), default=datetime.datetime.now())
    terminate_date = Column(TIMESTAMP())

    def __repr__(self):
        return f'{self.username}'

    @hybrid_property
    def password(self):
        return self.pwd_hash

    @password.setter
    def password(self, value):
        self.pwd_hash = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.pwd_hash, value)

class UserData(BaseModel):
    __tablename__ = 'users_data'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    first_name = Column(TEXT())
    last_name = Column(TEXT())
    email = Column(TEXT())
    birth_date = Column(TIMESTAMP())

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

class AuthHistory(BaseModel):
    __tablename__ = 'auth_history'

    user_id = Column(UUID(as_uuid=True),ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ip = Column(INET())
    user_agent = Column(TEXT())
    date_start = Column(TIMESTAMP())
    date_end= Column(TIMESTAMP())

    def __repr__(self):
        return f'{self.ip} {self.user_agent}'
