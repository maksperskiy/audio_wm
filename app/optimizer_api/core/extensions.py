from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.optimizer_api.core._settings import settings


def include_extensions(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
