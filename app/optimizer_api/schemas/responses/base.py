import datetime

from pydantic.main import BaseModel
from app.optimizer_api.services.utils import to_camel_case


class BaseResponse(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        json_encoders = {
            datetime.datetime: lambda x: x.replace(
                tzinfo=datetime.timezone.utc
            ).isoformat(timespec="seconds"),
        }
