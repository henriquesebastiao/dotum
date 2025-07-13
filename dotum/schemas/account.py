from datetime import date, datetime

from pydantic import BaseModel

from dotum.utils.enum import AccountType


class AccountBase(BaseModel):
    value: float
    description: str
    due_date: date
    account_type: AccountType
    paid: bool = False
    created_by: int
    created_at: datetime


class AccountCreate(AccountBase): ...


class AccountUpdate(BaseModel):
    value: float | None = None
    description: str | None = None
    due_date: date | None = None
    account_type: AccountType | None = None
    paid: bool | None = None
    created_by: int | None = None
    created_at: datetime | None = None


class AccountSchema(AccountBase): ...
