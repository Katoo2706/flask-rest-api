# Deploy with Render.com

![render-deployment.png](media%2Frender-deployment.png)

After deployment, web server will serve as 
![render-host.png](media%2Frender-host.png)

## Change env in Postman
![postman-vars.png](media%2Fpostman-vars.png)


## Health check
![render-health-check.png](media%2Frender-health-check.png)

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

# Auto-migration with docker-entrypoint.sh
