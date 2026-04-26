from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RedirectEventSchema(BaseModel):
    time: datetime = Field(..., description='Время в момент перехода по ссылке')
    slug: str = Field(..., description='Сокращенная ссылка')
    userinfo: str = Field(..., max_length=512, description='доп инфа про пользователя')

    model_config = ConfigDict(from_attributes=True)


class CreationEventSchema(BaseModel):
    time: datetime = Field(..., description='Время в момент создания сокращения')
    slug: str = Field(..., description='Сокращенная ссылка')
    userinfo: str = Field(..., max_length=512, description='доп инфа про пользователя')
    user_id: int = Field(..., description='id пользователя')

    model_config = ConfigDict(from_attributes=True)
