#FROM python:3.10
#
## Expose the port
#EXPOSE 5000
#
## Set up working directory
#WORKDIR /app
#
#COPY ./requirements.txt requirements.txt
#
#RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
#
#COPY . .
#
#CMD ["flask", "run", "--host", "0.0.0.0"]

# Set up with Gunicorn
FROM python:3.10

# Default port 80

# Set up working directory
WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]