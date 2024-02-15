from marshmallow import Schema, fields

"""
    PlainSchema is used to create nested field in other schema. 
    That's why we need to remove store_id = fields.Str(required=True)
    to make the dependent nested field (Make the connection).
"""


class PlainItemSchema(Schema):
    """
    Declare Item Schema, when we send data through Schema:
    - load_only:
        - Field will be used during deserialization (loading) but will be ignored when serializing (dumping).
        - Only used to receive data from clients.
    - dump_only:
        - Field will be used during serialization (dumping) but will be ignored when deserializing (loading).
        - Only used to return data to clients.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    # store_id = fields.Str(required=True)


class PlainItemUpdateSchema(Schema):
    """
    Not require any field because use can input price or name...
    """
    id = fields.Str(required=True)
    price = fields.Float()
    store_id = fields.Int()


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    # the field in schema must match the models
    stores = fields.Nested(PlainStoreSchema(), dump_only=True)  # nested schema from stores to make the connection

    # add nested field tags
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  # nested schema
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)  # nested schema


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainTagSchema(), dump_only=True)

    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class ItemTagSchema(Schema):
    """
    Many-to-many relationship (Tags & Items)
    Return when send data to clients
    """
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # not send to get method
