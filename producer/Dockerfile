# Header
FROM python:3.10
LABEL maintainer="murilo.fregonesi@gmail.com"

# Environment
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Application
EXPOSE 8000
ENTRYPOINT uvicorn app.main:app
