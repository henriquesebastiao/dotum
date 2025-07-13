from enum import Enum


class AccountType(str, Enum):
    PAYABLE = 'payable'
    RECEIVABLE = 'receivable'
