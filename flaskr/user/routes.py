from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from db import db
from flaskr.models import UserModel
from blocklist import BLOCKLIST

from schemas import UserSchema

blp = Blueprint("users", __name__, description="API for users")


@blp.route('/register')
class User(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=f"Can not insert user {e}")

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Check existing user
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            #
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(200, description="Delete an user",
                  examples={
                      "message": "User deleted"
                  })
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh the access token.
        :return: Access token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            "access_token": new_token
        }