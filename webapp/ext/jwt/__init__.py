from flask_jwt import JWT

from webapp.ext.auth.models import UserAuth
from webapp.ext.bcrypt import bcrypt


def authenticate(email, password):
    user = UserAuth.query.filter(UserAuth.email == email).scalar()
    if bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserAuth.query.get(user_id)


def init_app(app):
    jwt = JWT(app, authenticate, identity)
