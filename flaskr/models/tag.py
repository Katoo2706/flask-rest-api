from db import db


class TagModel(db.Model):
    """
    Model for Tags. Many-to-many relationship
    2 tag can have a same name.
    """
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(88), unique=True, nullable=False)
    store_id = db.Column(db.String(), db.ForeignKey("stores.id"), nullable=False)

    # relationship with other entities
    stores = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags",
                            secondary="items_tags")  # Association table that connects items and tags.
