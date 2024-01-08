FROM python:3.12-alpine as build
RUN apk add build-base
RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-alpine as final
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY car_iot car_iot
COPY thing.crt .
COPY *.key ./
COPY AmazonRootCA1.pem .

ENTRYPOINT ["python", "car_iot"]
