from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from flaskr.models import StoreModel

from schemas import StoreSchema

blp = Blueprint(name="Stores", import_name=__name__, description="API for Stores")


@blp.route('/store/<string:store_id>')
class StoreItem(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # retrieve by primary key. If no pk -> return 404
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Item deleted."}


@blp.route('/store')
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(schema=StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data: dict) -> dict:
        """
        Add the new store.
        Store data will be passed through Store Model.
        :param store_data: Body
        :return: Store datas
        """
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:  # duplicated id
            abort(400, message=f"Store name '{store.name}' already exists.")

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting data.")

        return store
