from ...exception.base_exception import DomainException


class EmailSendException(DomainException):
    def __init__(self, message: str, code: str = "EMAIL_SEND_FAILED"):
        super().__init__(message, code)
