FROM python:3.11

# Expose the port
EXPOSE 5000

# Set up working directory
WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]