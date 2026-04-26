from pydantic import BaseModel, Field
from datetime import datetime

class SlugSchema(BaseModel):
    slug: str = Field(..., description='Сокращенная ссылка')
    url: str = Field(..., description='Ссылка')


class NewSlugSchemaEvent(BaseModel):
    slug: str = Field(..., description='Сокращенная ссылка')
    url: str = Field(..., description='Ссылка')
    user_id: int = Field(..., description='id пользователя')
    userinfo: str = Field(..., max_length=512, description='доп инфа про пользователя')
    time: datetime = Field(..., description='Время в момент создания сокращения')
