from app.ai_api.database.models import ParamsModel
from app.ai_api.database.repositories.base import BaseRepository



class AIRepository(BaseRepository):
    __model__ = ParamsModel
