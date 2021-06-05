from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.sql import func

from webapp.ext.db import db


class UserAuth(UserMixin, db.Model):
    __tablename__ = "user_auth"

    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(255), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    created_on = db.Column(
        "created_on",
        db.DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    updated_on = db.Column(
        "updated_on",
        db.DateTime(timezone=True),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
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
