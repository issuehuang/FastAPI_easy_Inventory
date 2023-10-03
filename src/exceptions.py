'''
  Exceptions
'''
from fastapi import HTTPException, status
from typing import Any

# when request is scusess return
SCUSESS_MSG = {'detail': 'Scusess!'}


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class RequestTimeout(DetailedHTTPException):
    STATUS_CODE = status.HTTP_504_GATEWAY_TIMEOUT
    DETAIL = "Request timeout"


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class ServerError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str) -> None:
        self.DETAIL = detail
        super().__init__()


class CustomerNotFound(NotFound):
    DETAIL = "Customer not found"


class CustomerAlreadyExists(BadRequest):
    DETAIL = "Customer already exists"


class InvalidPasswordOrEmail(BadRequest):
    DETAIL = "Invalid password or email"


class CredentialsDataWrong(NotAuthenticated):
    DETAIL = "Could not validate credentials"


class ItemAlreadyExists(BadRequest):
    DETAIL = "Item already exists"


class ItemNotFound(NotFound):
    DETAIL = "Item not found"


class NotAdmin(PermissionDenied):
    DETAIL = "Not admin"


class ItemNotEnoughQuantity(BadRequest):
    DETAIL = "Item not enough quantity"
