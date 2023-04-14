import datetime

from pydantic import BaseModel
from app.optimizer_api.services.utils import to_camel_case


class BaseRequest(BaseModel):
    class Config:
        alias_generator = to_camel_case
        json_encoders = {
            datetime.datetime: lambda x: x.replace(
                tzinfo=datetime.timezone.utc
            ).isoformat(timespec="seconds"),
        }
