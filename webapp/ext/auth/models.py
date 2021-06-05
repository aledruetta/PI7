from datetime import datetime
from flask_login import UserMixin

from webapp.ext.db import db


class UserAuth(UserMixin, db.Model):
    __tablename__ = "user_auth"

    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(255), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    created_on = db.Column("created_on", db.DateTime, default=datetime.now)
    updated_on = db.Column("updated_on", db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_admin = db.Column("is_admin", db.Boolean, default=False)

    def json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "created_on": datetime.timestamp(self.created_on),
            "updated_on": datetime.timestamp(self.updated_on),
            "is_admin": self.is_admin,
        }

    def __repr__(self) -> dict:
        return f"User: {self.email} {'(Admin)' if self.is_admin else ''}"
