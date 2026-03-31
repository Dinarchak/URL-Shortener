from pydantic import BaseModel, Field
from datetime import datetime

class RedirectInfo(BaseModel):
    slug: str = Field(..., description="Сокращенная ссылка")
    time: datetime = Field(..., description="Время перехода")
    userinfo: str = Field(..., description="Доп инфа про юзера")
