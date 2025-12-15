from pydantic import BaseModel, Field
from datetime import datetime

class SlugSchema(BaseModel):
    slug: str = Field(..., description='Сокращенная ссылка')
    url: str = Field(..., description='Ссылка')


class CreateLinkSchema(BaseModel):
    url: str = Field(..., description='Ссылка')