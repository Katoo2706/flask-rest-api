# CONTRIBUTING

## Run with docker without gunicorn
## Deploy with docker-compose
> If we change the code, the Flask app will be refreshed

To rebuild the image after add new packages for python
```bash
docker-compose up --build
```

## How to run the Dockerfile locally

Build image
```bash
docker build -t rest-api-recording-email .
```

Run service
```bash
# docker run --name <container_name> -p 5000:5000 -w /app -v "$(pwd):/app" <IMAGE_NAME> sh -c "flask run --host 0.0.0.0"

docker run --name flask-api -p 5000:5000 -w /app -v "$(pwd):/app" rest-api-recording-email sh -c "flask run --host 0.0.0.0"
```

Run rq worker. Connect redis to rq worker
```bash
docker run -w /app rest-api-recording-email sh -c "rq worker -u <redis_Url> <app_queue>"

# app_queue can be "emails"
```


