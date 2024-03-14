# Flask REST API

> Healthcheck: 

Project structure
```markdown
/project-root
│
├── app.py
├── db.py
├── flaskr
│   ├── __init__.py
│   ├── static
│   ├── templates
│   ├── utils
│   │   └── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── stores.py
│   ├── items
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── stores
│       ├── __init__.py
│       └── routes.py
```
- `app.py` is the main entry point for your Flask application.
- `db.py` could be used to manage database connections or configurations.
- `flaskr` is the package that contains the main application module.
  - `static` is the directory for static files (e.g., CSS, JavaScript).
  - `templates` is the directory for HTML templates.
  - `utils` is a package that can contain utility functions or modules.
  - `models` is a package that contains modules defining your data models.
  - `items` and stores are packages for organizing routes related to items and stores.

For HTTP requests:
- Header:
  - `Content-Type`: `application/json` (automatically if we use json body)

If we run a Flask app, variables will store the memory :) we can get or post with dictionary stores.

In production, we should clear Flask's Memory Cache

## Debug mode
Run Flask app in debug mode
```bash
flask --debug run --host=0.0.0.0
```

Or set env
```bash
FLASK_DEBUG=1
```

## Log console to file
```bash
from flask import Flask
import logging

app = Flask(__name__,
            static_folder='./flaskr/static',
            template_folder='./flaskr/templates')

# Configure Flask logging
# https://docstrings.wordpress.com/2014/04/19/flask-access-log-write-requests-to-file/
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)
```

## Sample request
### Post request
- Can not `return None` or `pass`

## Route parameters
Reference: https://pythonbasics.org/flask-tutorial-routes/

Parameters in route name can be `param` or `<datatype:param>` (`/<int:year>/<int:month>/<string:title>`)

### flask route params
Parameters can be used when creating routes. A parameter can be a string (text) like this: /product/cookie.

![example_request.png](media%2Fexample_request.png)

That would have this route and function:
```
@app.route('/product/<name>')
def get_product(name):
  return "The product is " + str(name)
```

### flask route multiple arguments
If you want a flask route with multiple parameters that’s possible. For the route /create/<first_name>/<last_name> you can do this:
```
@app.route('/create/<first_name>/<last_name>')
def create(first_name=None, last_name=None):
  return 'Hello ' + first_name + ',' + last_name
```

## flask-smorest
- Serialization, deserialization and validation using marshmallow Schema
- Explicit validation error messages returned in response
```
return {"message": "Object not found"}, 404

-> update to

from flask_smorest import abort
abort(404, message="Store not found")

or we just need abort from flask
from flask import abort
abort(404, description="Store not found")
```
- Database-agnostic
- OpenAPI (Swagger) specification automatically generated and exposed with ReDoc, Swagger UI or RapiDoc
- Pagination
- ETag

## Blue print
## Swagger API documents server
### Method 1: Manually documents server
Add `flaskr/static/swagger.json`

Swagger editor ref: https://editor.swagger.io/

Config in app.py
```markdown
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__,
            static_folder='./flaskr/static',
            template_folder='./flaskr/templates')

SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    base_url='/document',
    api_url='/static/swagger.json',
    config={
        'app_name': "Kato API document site"
    }
)
app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix='/document')

```

### Method 2: flask_smorest will help us to build Swagger UI 
```markdown
from flask import Flask
from flask_smorest import Api

from flaskr.items import blp as ItemBlueprint
from flaskr.stores import blp as StoreBlueprint

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

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

```

## Flask Blueprint
> Each Flask Blueprint is an object that works very similarly to a Flask application. They both can have resources, such as static files, templates, and views that are associated with routes.

> However, a Flask Blueprint is not actually an application. It needs to be registered in an application before you can run it

```markdown
from flask_smorest import Blueprint

blp = Blueprint("Stores", __name__, description="API for Stores")

@blp.route('/store/<string:store_id>')
def get_stores(store_id):
    return stores[store_id]

@blp.route('/store')
class ItemList(MethodView):
  def get(self):
      return stores
```

then in app.py, we just need to register_blueprint
```markdown
from flask import Flask
from flask_smorest import Api

from flaskr.items import blp as ItemBlueprint
from flaskr.stores import blp as StoreBlueprint

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

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

```

Docs from method in Blueprint
```markdown
    def post(self):
        """ This will be a short description in Swagger ui
            - Input:
            {
                "store_id": "Store_id",
                "name: "xxx",
                "price: "...,
                ...
            }
            """
```

![swagger-ui.png](media%2Fswagger-ui.png)

## Methodview
> MethodView is a class within the flask.views module of the Flask project. MethodView is a Python Metaclass that determines the methods, such as GET, POST, PUT, etc, that a view defines.

Instead of we declare multi method with same route, we can use MethodView to declare `GET`, `POST`, `PUT`, etc in a single Class. 

```markdown
@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        return 1

    def delete(self, store_id):
        return 1
```

## Marshmallow Schema
> Marshmallow uses classes to define output schemas. This allows for easy code reuse and configuration. 
> Each schema can represent for each Class in Blueprint

### 1. Declare schema by class in schemas.py
Declare Item Schema, when we send data through Schema:
- `load_only`: Field will be used during deserialization (loading) but will be ignored when serializing (dumping).
- `dump_only`: Field will be used during serialization (dumping) but will be ignored when deserializing (loading).
- ...

Reference: https://marshmallow.readthedocs.io/en/stable/api_reference.html

### 2. Add schema for each blueprint method
Instead of doing:
```markdown
def post(self):
    item_data = request.get_json()
    if not all(key in item_data for key in ['price', 'store_id', 'name']):
        abort(400,
              description="Bad request. Ensure 'price', 'store_id', and 'name' are included in JSON payload")
    for item in items.values():
        ...
```

We can decorate the method `@blp.arguments(schema=ItemSchema)` and add argument `data` to method:
```markdown
from schemas import ItemSchema

@blp.arguments(schema=ItemSchema)
def post(self, item_data):
    for item in items.values():
          ...
``` 
- Json data from clients will be passed through `ItemSchema`.
- It will be validated before sends data to method.
- We don't need `data = request.get_json()` anymore

Schema information will be also shown on Swagger UI
![swui-schema.png](media%2Fswui-schema.png)

### 3. Decorating response with flask_smorest
- Specifies the expected structure of the method's response, including HTTP status code and data format.
- Enhances API documentation and maintains consistency for developers and clients consuming the API.

Define what to send.
```markdown
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, description="Item not found.")
```

Note: `blp.response` decorator will be after `blp.arguments`. 
```markdown
@blp.arguments(ItemUpdateSchema)
@blp.response(200, ItemSchema)
def put(self, item_data, item_id):
    ...
```

Response as List if we set `many=True`
```markdown
@blp.response(200, ItemSchema(many=True))
    def get(self):
        return {
            "items": list(items.values())
        }
```

Because we use dump_only, the _id field won't be sent to client
```markdown
class ItemSchema(Schema):
    """
    Declare Item Schema, when we send data through Schema:
    - load_only: Field will be used during deserialization (loading) but will be ignored when serializing (dumping).
    - dump_only: Field will be used during serialization (dumping) but will be ignored when deserializing (loading).
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

```

Document other responses
```markdown
@blp.response(200, description="Delete a tag")
@blp.alt_response(404, description="Tag not found")
@blp.alt_response(400, description="Return if the tag is assigned to one or more items".)
def delete(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)

    # if tag is not assigned with any item
    if not tag.items:
        db.session.delete(tag)
        db.session.commit()

        return {"message": "Tag deleted."}

    abort(400,
          message="Could not delete tag, remote tag from items first")

```

## SQL Alchemy extension
> `flask-sqlalchemy`

Object Relational Mapping (ORM) is a technique used in creating a "bridge" between object-oriented programs and, in most cases, relational databases.

1. Define db in db.py
2. Create `models` folder in `flaskr`.
3. Define the data types: [Reference](https://docs.sqlalchemy.org/en/20/core/types.html)
```python
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
    price = db.Column(db.Float(precision=2), unque=False, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),  # map stores.id as Foreign key
                         unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")  # Define the relationship with StoreModel class
```
4. We need to define both foreign key and relationship between 2 Models. [Relationship API](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)
5. Reflect in schemas.py: After that, we need to update `schemas.py` to add PlainSchema & Schema to add the relationship 
Create nested field
```markdown
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
```
6. Import models into app.py
- Models tell flask what table, column need to be created
```markdown
import flaskr.models

# Config SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # improve sqlalchemy performance
```
7. Create all table before first request (Instead, we can use flask-migrate)
```markdown
@app.before_request
def create_table():
    db.create_all()

-> deprecated

with app.app_context():
    db.create_all()
```
### Define SQLAlchemy models. 
```python
from db import db


class ItemModel(db.Model):
    """
        - __tablename__: Table name in database
        - id, name, price, store_id: Column name. (store_id is foreign key of table stores.id)
        - stores = db.relationship("StoreModel", back_populates="items"):
            - when we access stores, we can get the stores list that this item belong to
            - define the connection between StoreModel and ItemModel
    """
    __tablename__ = "items"

    # Define the column
    # https://docs.sqlalchemy.org/en/20/core/types.html
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),  # map stores.id as Foreign key
                         unique=False, nullable=False)
    # Stores mapping must exist in ItemModel - mapping between 2 model. And must be defined in schemas.py
    stores = db.relationship("StoreModel", back_populates="items")  # Define the relationship with StoreModel class

```

### Query from SQLAlchemy
> Retrieve by primary key. If no pk -> return 404

```markdown
@blp.route('/store/<string:store_id>')
class StoreItem(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
```

### Put method - Update data with SQLAlchemy

### Query all
```markdown
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # items = ItemModel.query
        return ItemModel.query.all()
```

### Delete
```markdown
db.session.delete(store)
```

### Delete related models with CASCADES
> To ignore the null foreign key, we need to delete CASCADES

Update in models `store` -> set up with delete store -> all item disappear
```markdown
items = db.relationship("ItemModel", back_populates="stores",
                            lazy="dynamic", cascade="all, delete"
                            # items not be fetched util we query
                            )
```

### Many-to-many Relationship
#### Stores with tags
![manymany.png](media%2Fmanymany.png)
[Tags will be an entity in the database]

- Add the Tagmodel, Set the foreign key to StoreModel
- Add nested field in StoreModel
```markdown
tags = db.relationship("Tagmodel", back_populates="store", lazy="dynamic")
```
- Add TagSchema into schemas.py
- Then create blueprint for Tags

#### Item with tags.
- Create [items_tags.py](flaskr%2Fmodels%2Fitems_tags.py)
- Add nested field in `tags` model & `items" model

Secondary tables" 
```markdown
items = db.relationship("ItemModel", back_populates="tags", secondary="item_tags")
```

```markdown
# in items schema
tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
```

```markdown
# in tags schema
items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
```

Define ItemTagSchema
```markdown
class ItemTagSchema(Schema):
    """
    Many-to-many relationship (Tags & Items)
    """
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())
```
Return with delete method
```markdown
return {"message": "Item remove from tags",
        "item": item,
        "tag": tag}
```

- Then add the blue print into tags/routes.py

## JWT
![jwt.png](media%2Fjwt.png)

![jwt-time.png](media%2Fjwt-time.png)

> package: flask-jwt-extended

```python
from flask_jwt_extended import JWTManager


# Config JWT manager
app.config["JWT_SECRET_KEY"] = "your_secret_key_value"
jwt = JWTManager(app)
```
- Secret keu is used for signing the JWTs.
- Not same as encryption, JWT use secret key to check who send the request
- In python, we can generate random secret key to make it safe.
```python
import secrets

app.config["JWT_SECRET_KEY"] = secrets.SystemRandom().getrandbits(128)
```
- If we don't want to change secret key when restart the app, regenerate, copy and paste into the app.

### Create UserModel & UserSchema with JWT extension
- Create Blueprint for User registration
- Hash user password `pbkdf2_sha256.hash(user_data["password"])` with package `passlib`
- When user login, verify the password `pbkdf2_sha256.verify(user_data["password"], user.password)`

### Create access token to validate user
- Treat `access_token` as proxy for user log in
- Create `/login` endpoint to return access token to user
![login-return-access-token.png](media%2Flogin-return-access-token.png)
- The `access_token` can be decoded here to see the information: https://jwt.io/
- The user can send jwt to server for validation
- Having JWT means being able to impersonate the user who the JWT was created for.

### Update endpoints to request access_token for API request
- Update `flaskr/item/routes.py` to require JWT for any request
- Add `@jwt_required()` decorator for each request
```markdown
from flask_jwt_extended import jwt_required

@jwt_required()
@blp.response(200, ItemSchema(many=True))
def get(self):
    # items = ItemModel.query
    return ItemModel.query.all()
```
- Request need to include jwt token
![request.png](media%2Frequest.png)

> JWT can be expired. We should add error handler
Manage expiration time for JWT in app.py
```markdown
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
```

**Modify the error message for JWT in app.py:**
- Add configuration. The jsonify function is then used to convert this dictionary into a JSON-formatted response
> Using jsonify provides clarity, flexibility, and additional control over your JSON responses, making your code more maintainable and easier to understand.

### JWT claims and authorization
- To authorize admin user and be able to do delete method
```markdown
# in app.py
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}
```
- In `flaskr`, user `get_jwt()` to get jwt content
```markdown
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def delete(self, item_id):
    jwt = get_jwt()
    if not jwt.get("is_admin"):
        abort(401, message="Admin privilege required.")
```

### Log out the Rest API / Revoke the access token
- Check in jwt in blocklist.py -> revoked token -> raise error
- In app.py
```markdown
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
```
- Then create `/logout` endpoint for user to logout

### Token refreshing
> Instead of asking users to re-authenticate, we can get the client to get new token for us without asking for username & password: 
> [routes.py](flaskr%2Fuser%2Froutes.py)

Create refresh token and set refesh=True for access token
```markdown
from flask_jwt_extended import create_access_token, create_refresh_token

# If this token should be marked as fresh, and can thus access endpoints
# protected with `@jwt_required(fresh=True)`. Defaults to `False`.
access_token = create_access_token(identity=user.id, fresh=True)
refresh_token = create_refresh_token(identity=user.id)
```
For example, this method require fresh=True. In [routes.py](flaskr%2Fitem%2Froutes.py):
```markdown
@jwt_required(fresh=True)
def delete(self, item_id):
```
Add another loader when receive non-fresh token
```markdown
# app.py
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
```

- User can refresh token if access_token expired
![refresh-token.png](media%2Frefresh-token.png)

### Request chaining with Isomnia - Postman
> To get the variable as response from other request :D
![create-global-var.png](media%2Fcreate-global-var.png)
> User variable in the request as {{variable_name}}
![chain-request.png](media%2Fchain-request.png)

## Flask Migration
> SQLAlchemy database migrations for Flask applications using [Alembic](https://pypi.org/project/alembic/).: `flask-migrate`.

### Initial database with Flask Migrate
1. Create migration for db or emable migration
```bash
flask db init
```
- versions: Changed to database
- alembic.ini: Configuration file
- env.py: Generate migration file

2. Generate an initial migration (compare db with models to add the migrations):
```bash
flask db migrate
```

3. Apply the migration to the database:
```bash
flask db upgrade
```

Note: With flask-migrate, we don't need to create table before first request. It might cause a conflict with the flask-migrate.

### Change SQLAlchemy model and generate migrations
If we change the SQLAlchemy model, we need to log in the database, update the database with SQL code.

Instead, Flask-migrate will help use to make the changes to database.
```bash
# Generate the migration
flask db migrate
```
Console logging:
```markdown
INFO  [alembic.autogenerate.compare] Detected added column 'items.description'
```
```bash
# Upgrade the migration
flask db upgrade
```

### Manually review and modify database migrations
- When insert new column to database. Previous row will be null. If we set nullable=False => error in migration. 
- We should reivew the migration code. [versions](migrations%2Fversions)
![review-migration.png](media%2Freview-migration.png)