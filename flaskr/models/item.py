from db import db


class ItemModel(db.Model):
    """
        Tell sqlalchemy that we want to create / use table "items
    """
    __tablename__ = "items"

    # Define the column
    # https://docs.sqlalchemy.org/en/20/core/types.html
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=5), unique=False, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),  # map stores.id as Foreign key
                         unique=False, nullable=False)

    # Create relationship
    stores = db.relationship("StoreModel", back_populates="items")  # Define the relationship with StoreModel class
    tags = db.relationship("TagModel", back_populates="items",
                           secondary="items_tags")  # Association table that connects items and tags.
