from flask_jwt import JWT
from bcrypt import check_password_hash

from webapp.ext.auth.models import UserAuth


def authenticate(email, password):
    user = UserAuth.query.filter(UserAuth.email == email).scalar()
    if check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserAuth.query.get(user_id)


def init_app(app):
    jwt = JWT(app, authenticate, identity)
