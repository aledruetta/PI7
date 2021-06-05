from flask_restful import Api

from webapp.ext.api.views import ApiThing, ApiThingAll, ApiUser, ApiUserAll

api = Api()


api.add_resource(ApiUserAll, "/api/user")
api.add_resource(ApiUser, "/api/user/<string:user_id>")
api.add_resource(ApiThingAll, "/api/thing")
api.add_resource(ApiThing, "/api/thing/<string:thing_id>")


def init_app(app):
    api.init_app(app)
