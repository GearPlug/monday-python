class BaseError(Exception):
    pass


class UnauthorizedError(BaseError):
    pass


class WrongFormatInputError(BaseError):
    pass


class ContactsLimitExceededError(BaseError):
    pass