FROM python:3.7-alpine
ADD . /code
WORKDIR /code
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
