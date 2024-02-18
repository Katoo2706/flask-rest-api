import os
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from flaskr.models import UserModel
from schemas import UserSchema, UserRegisterSchema

# Task queue
import redis
from rq import Queue
from flaskr.utils import send_welcome_email

blp = Blueprint("users", __name__, description="API for users")

# App Queue with Redis
connection = redis.from_url(
    os.getenv("REDIS_URL"))
queue = Queue("emails", connection=connection)


@blp.route('/register')
class User(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        # Check unique email
        if UserModel.query.filter(
                or_(
                    UserModel.username == user_data["username"],
                    UserModel.email == user_data["email"]
                )
        ).first():
            abort(400, message="User / email already exist")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            email=user_data["email"]
        )
        try:
            db.session.add(user)
            db.session.commit()

            # send simple message with task queue
            queue.enqueue(send_welcome_email, user.email, user.username)

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
