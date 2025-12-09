from pydantic import BaseModel, Field
from datetime import datetime

class LinkSchema(BaseModel):
    short_url: str = Field(..., description='Сокращенная ссылка')
    url: str = Field(..., description='Ссылка')
    user_id: int = Field(..., description='id пользователя, создавшего сокращение')
    expires_at: datetime = Field(..., description='Срок ссылки')


class CreateLinkSchema(BaseModel):
    short_url: str = Field(..., description='Сокращенная ссылка')
    url: str = Field(..., description='Ссылка')
    user_id: int = Field(..., description='id пользователя, создавшего сокращение')
    created_at: datetime = Field(..., 'Время создания ссылки')
