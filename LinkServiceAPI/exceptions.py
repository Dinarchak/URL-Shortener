class ShortenerBaseException(Exception):
    pass


class SlugAlreadyExistsError(Exception):
    pass


class NotUrlFindError(Exception):
    pass


class EventSendingError(Exception):
    pass