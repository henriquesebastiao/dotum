from datetime import date

from pydantic import BaseModel

from dotum.utils.enum import AccountType


class AccountBase(BaseModel):
    value: float
    description: str
    due_date: date
    account_type: AccountType
    paid: bool = False
    created_by: int


class AccountCreate(AccountBase): ...


class AccountUpdate(BaseModel):
    value: float | None = None
    description: str | None = None
    due_date: date | None = None
    account_type: AccountType | None = None
    paid: bool | None = None


class AccountSchema(AccountBase): ...


class AccountInformation(BaseModel):
    value: float
    description: str
    due_date: date
    account_type: AccountType
    paid: bool


class AccountList(BaseModel):
    accounts: list[AccountInformation]


class TotalAccounts(BaseModel):
    total: float
