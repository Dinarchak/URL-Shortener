from schemas import RedirectEventSchema
from sqlalchemy.exc import SQLAlchemyError
from exceptions import RedirecEventRecordingException
from dao import add_redirect_event_record, get_all_event_records
from typing import List

async def add_redirect_event(event: RedirectEventSchema):
    try:
        await add_redirect_event_record(
            slug = event.slug,
            time = event.time,
            userinfo = event.userinfo
        )
    except SQLAlchemyError as e:
        raise RedirecEventRecordingException(str(e))

async def get_all_events() -> List[RedirectEventSchema]:
    res = await get_all_event_records()
    return [RedirectEventSchema.model_validate(obj) for obj in res]
