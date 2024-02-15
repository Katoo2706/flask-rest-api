from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Stores mapping must exist in ItemModel - mapping between 2 model
    items = db.relationship("ItemModel", back_populates="stores",
                            lazy="dynamic", cascade="all, delete"
                            # items not be fetched util we query
                            )

    tags = db.relationship("TagModel", back_populates="stores", lazy="dynamic")
