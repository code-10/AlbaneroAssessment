from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from flaskapp.sqlite_database import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=True)
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="user")

    def generate_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

from flaskapp.train.models import Ticket
