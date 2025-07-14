from pydantic import BaseModel

from dotum.utils import message


class BaseRaiseModel(BaseModel):
    detail: str


class EmailAlreadyExists(BaseRaiseModel):
    detail: str = message.AlreadyExists.EMAIL


class EmailOrUsernameAlreadyExists(BaseRaiseModel):
    detail: str = message.AlreadyExists.EMAIL_OR_USERNAME


class UserDoesNotExists(BaseRaiseModel):
    detail: str = message.DoesNotExist.USER
