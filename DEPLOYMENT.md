# Deploy with Render.com
Render will create an external API for us with that endpoints.
![render-deployment.png](media%2Frender-deployment.png)

After deployment, web server will serve as 
![render-host.png](media%2Frender-host.png)

## Change env in Postman
![postman-vars.png](media%2Fpostman-vars.png)


## Health check
![render-health-check.png](media%2Frender-health-check.png)

Request: https://rest-apis-flask-docker.onrender.com/

# Using Gunicorn in Docker
> Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.
> Additional package: `gunicorn`
> 
> Reference: https://gunicorn.org/

## Update Dockerfile and push changes
```Dockerfile
WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
```

# PostgreSQL backend database
> We use [ElephantSQL](https://www.elephantsql.com/) as a Database service
> Additional package: `psycopg2-binary` 

Then use load_dotenv to load db_url in `app.py`

```python
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")
```

## Auto-migration
docker-entrypoint.sh
```bash
#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"
```

## Create free Redis database
![redis-db.png](media%2Fredis-db.png)

## Get the access
- Change listening port to 0.0.0.0/0 (not /32)
- Copy External Redis URL
![redis-connection.png](media%2Fredis-connection.png)

# Sending email with SMTPlib & Jinja2
> Package: Jinja2
> 
> Email template `Mailgun`: https://github.com/mailgun/transactional-email-templates

When user send request to `/register`, after registration, we will send an email to confirm to user

Reference: [emails.py](flaskr%2Futils%2Femails.py)
- Jinja will pass username into [welcome.html](flaskr%2Ftemplates%2Fwelcome.html) using render_html method [render_html.py](flaskr%2Futils%2Frender_html.py)
- Add field email to UserModel & UserSchema. Then run `flask db migrate` & `flask db upgrade`. We might get this error `(psycopg2.errors.NotNullViolation) column "email" contains null values`
![migrate.png](media%2Fmigrate.png)
[We should change `None` to `String value` in migrations/versions (e.g: "email") or update value for column "emails" in database]
- When user register successfully, we will send a welcome email to use 

# Set up Task queue with Redis database
> Package: `rq`, `redis`
![redis.png](media%2Fredis.png)

Config in `/register` endpoint
```python
# Task queue
from rq import Queue
import redis
import os
from flaskr.utils import send_welcome_email

blp = Blueprint("users", __name__, description="API for users")

# App Queue with Redis
connection = redis.from_url(
    os.getenv("REDIS_URL"))
queue = Queue(name="emails", connection=connection)


# send simple message with task queue in /register
queue.enqueue(send_welcome_email, user.email, user.username)
```

Otherwise, without task queue, we can just use
```markdown
send_welcome_email(user.email, user.username)
```

## Run background worker

Run rq worker. Connect redis to rq worker
```bash
docker run -w /app rest-api-recording-email sh -c "rq worker -u <redis_Url> <app_queue>"

# app_queue can be "emails"
```

## Deploy background worker to render.com
> Note: We can use internal url for Var Env in Render.com to access Reddit database.

1. Add [settings.py](settings.py) to root
2. Add Background worker in Render.com
![render-background-worker.png](media%2Frender-background-worker.png)
- Add Redis URL variable
3. Add docker command for deployment
![render-background-worker-2.png](media%2Frender-background-worker-2.png)