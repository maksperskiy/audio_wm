from fastapi import FastAPI

from app.optimizer_api.api.views import router
from app.optimizer_api.core import Constants, include_extensions


def create_app():
    app_ = FastAPI(
        version="1.2.1",
        openapi_url=f"{Constants.APP_PREFIX}/openapi.json",
        title=Constants.APP_TITLE,
        docs_url=f"{Constants.APP_PREFIX}/docs",
        redoc_url=f"{Constants.APP_PREFIX}/redoc",
    )
    app_.include_router(router)
    include_extensions(app_)
    return app_


app = create_app()
