import datetime
import hashlib
from typing import TypeVar

import bcrypt
from sqlalchemy import (BOOLEAN, TEXT, TIMESTAMP, VARCHAR, Column, ForeignKey,
                        LargeBinary)
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.ext.hybrid import hybrid_property

from src.db.models.base import BaseModel

UT = TypeVar('UT')
UDT = TypeVar('UDT')
AHT = TypeVar('AHT')


class PasswordConstants:  # noqa
    algorithm = 'sha256'
    iterations = 100000


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = ({'extend_existing': True},)

    username = Column(VARCHAR(255), nullable=False, unique=True)
    pwd_hash = Column(LargeBinary(), nullable=False)
    is_superuser = Column(BOOLEAN(), default=False)
    data_joined = Column(TIMESTAMP(), default=datetime.datetime.now)
    terminate_date = Column(TIMESTAMP(), nullable=True)

    def __repr__(self):
        return f'{self.username}'

    @hybrid_property
    def password(self):
        return self.pwd_hash

    @password.setter
    def password(self, value: str):
        salt = bcrypt.gensalt()
        self.pwd_hash = hashlib.pbkdf2_hmac(
            PasswordConstants.algorithm,
            value.encode('utf-8'),
            salt,
            PasswordConstants.iterations,
        ) + b'$' + salt

    def check_password(self, value: str):
        received_salt = self.pwd_hash[-29:]
        received_pwd_hash = hashlib.pbkdf2_hmac(
            PasswordConstants.algorithm,
            value.encode('utf-8'),
            received_salt,
            PasswordConstants.iterations,
        ) + b'$' + received_salt

        return self.pwd_hash == received_pwd_hash


class UserData(BaseModel):
    __tablename__ = 'users_data'
    __table_args__ = ({'extend_existing': True},)

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    first_name = Column(TEXT())
    last_name = Column(TEXT())
    email = Column(TEXT())
    email_confirmed = Column(BOOLEAN(), default=False)
    birth_date = Column(TIMESTAMP())

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class AuthHistory(BaseModel):
    __tablename__ = 'auth_history'
    __table_args__ = ({'extend_existing': True})

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    ip = Column(INET(), nullable=False)
    user_agent = Column(TEXT(), nullable=False)
    date_start = Column(TIMESTAMP(), default=datetime.datetime.now)
    date_end = Column(TIMESTAMP(), default=None)

    def __repr__(self):
        return f'{self.ip} {self.user_agent}'
