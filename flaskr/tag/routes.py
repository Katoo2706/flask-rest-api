from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from flaskr.models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, ItemTagSchema

blp = Blueprint("Tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """
        Query all the tags belonging to a specific store
        -> then return a dynamic field: tags
        Use all(): for the query

        :param store_id:
        :return:
        """
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        """

        :param tag_data: Body of the request
        :param store_id: parameter from the url
        :return:
        """
        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
        #     abort(400, message="Existing tag in that store")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,
                  message=str(e))

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        #  Add tag into tags list (item data)
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred")

        return item

    @blp.response(200, ItemTagSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        #  Add tag into tags list (item data)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred")

        return {"message": "Item remove from tags",
                "item": item,
                "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    @blp.response(
        200,
        description="Deletes a tag if no item, is tagged with it.",
        examples={
            "message": "Tag deleted."
        }
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Return if the tag is assigned to one or more items")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        # if tag is not assigned with any item
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"message": "Tag deleted."}

        abort(400,
              message="Could not delete tag, remote tag from items first")
