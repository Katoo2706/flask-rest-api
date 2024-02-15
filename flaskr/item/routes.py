from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from flaskr.models import ItemModel
from schemas import ItemSchema, PlainItemUpdateSchema

# JWT require
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Items", __name__, description="API for Items")  # description to show up in the Swagger UI


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Query in the database or response 404 not found
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(PlainItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """
        Update or add the item
        :param item_data:
        :param item_id:
        :return:
        """
        item = ItemModel.query.get_or_404(item_id)
        if item:
            """
                If the item exists, jut need field price & name
                -> do update the item
            """
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            """
                If item not exists -> get the data
                - Specify the id from the url request
            """
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {e}")


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(schema=ItemSchema)
    @blp.response(200, ItemSchema(many=True))
    def post(self, item_data):
        """ This will be a short description in Swagger ui
            - Input:
            {
                "store_id": "Store_id",
                "name: "xxx",
                "price: "...,
                ...
            }

            Instead of data validation by if statement, we can use registered schema
            @blp.arguments(schema=ItemSchema):
            - Json from clients will be parsed into ItemSchema and will be validated
            - User ItemModel to manage the table in database and check I/O data
            """

        # pass all the value as key-arguments into the Item Model
        item = ItemModel(**item_data)
        try:
            # Use SQLAlchemy to import data
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=f"Can not insert item {e}")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting data")

        return item
