from schemas import RedirectEventSchema, CreationEventSchema
from sqlalchemy.exc import SQLAlchemyError
from exceptions import RedirecEventRecordingException, CreateEventRecordingException
from dao import (
    add_redirect_event_record,
    get_all_redirect_event_records,
    add_create_event_record,
    get_all_create_event_records
    )
from typing import List

async def add_redirect_event(event: RedirectEventSchema):
    try:
        await add_redirect_event_record(
            slug=event.slug,
            time=event.time,
            userinfo=event.userinfo
        )
    except SQLAlchemyError as e:
        raise RedirecEventRecordingException(str(e))

async def get_all_redirect_events() -> List[RedirectEventSchema]:
    res = await get_all_redirect_event_records()
    return [RedirectEventSchema.model_validate(obj) for obj in res]

async def add_create_event(event: CreationEventSchema):
    try:
        await add_create_event_record(
            slug=event.slug,
            time=event.time,
            userinfo=event.userinfo,
            user_id=event.user_id
        )
    except SQLAlchemyError as e:
        raise CreateEventRecordingException(str(e))

async def get_all_redirect_events_by_user(user_id: int) -> List[CreationEventSchema]:
    res = await get_all_create_event_records(user_id=user_id)
    return [CreationEventSchema.model_validate(obj) for obj in res]

async def get_all_redirect_events() -> List[CreationEventSchema]:
    res = await get_all_create_event_records()
    return [CreationEventSchema.model_validate(obj) for obj in res]
