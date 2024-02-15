from flask import Flask, jsonify
from flask_smorest import Api
import os

from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST

# Flask migration
from flask_migrate import Migrate

from flaskr.item import blp as ItemBlueprint
from flaskr.store import blp as StoreBlueprint
from flaskr.tag import blp as TagBlueprint
from flaskr.user import blp as UserBlueprint


def create_app():
    app = Flask(__name__,
                static_folder='./flaskr/static',
                template_folder='./flaskr/templates')

    app.config["PROPAGATE_EXCEPTIONS"] = True  # The error will be re-raised so that the debugger can display it
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Config SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # improve sqlalchemy performance
    db.init_app(app)

    # Config flask migrate
    migrate = Migrate(app=app, db=db)

    api = Api(app)

    # Config JWT manager
    app.config["JWT_SECRET_KEY"] = "317388865638347410416060922406110585170"
    jwt = JWTManager(app)

    # JWT error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """

        :param jwt_header: Extracted from jwt content
        :param jwt_payload Extracted from jwt content
        :return:
        """
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """

        :param error: No JWT received
        :return:
        """
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # JWT claims & authorization
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """
        Look into the database and see whether user is an admin (user/id)
        :param identity: From access_token = create_access_token(identity=user.id)
        :return:
        """
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    # Revoke token
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload) -> bool:
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {"description": "the Token has been revoked",
             "error": "token_revoked"}
        ), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # # Create db instance before first request
    # with app.app_context():
    #     db.create_all()

    @app.get('/')
    def health_check():
        return "Ok"

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    app.register_blueprint(TagBlueprint)
    app.register_blueprint(UserBlueprint)

    return app
