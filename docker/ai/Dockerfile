FROM python:3.9-slim as base

RUN mkdir /app 

COPY docker/ai/requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

FROM base as app

# WORKDIR /app/

COPY ./app/ai_api/ /app/ai_api/

EXPOSE 80

ENV PYTHONPATH=/
ENTRYPOINT ["uvicorn", "app.ai_api.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]