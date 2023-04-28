FROM python:3.9-slim as base

RUN mkdir /app 

COPY docker/optimizer/requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN apt-get update
RUN apt-get install -y fftw3 fftw3-dev pkg-config

FROM base as app

# WORKDIR /app/

COPY ./app/optimizer_api/ /app/optimizer_api/
COPY ./data/fold2/ /data/fold2/

EXPOSE 80

ENV PYTHONPATH=/
ENTRYPOINT ["uvicorn", "app.optimizer_api.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]