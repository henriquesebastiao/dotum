from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from dotum.utils.enum import AccountType

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    accounts: Mapped[List['Account']] = relationship(
        back_populates='user',
        lazy='immediate',
        init=False,
        default_factory=list,
    )


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    value: Mapped[float]
    description: Mapped[str]
    due_date: Mapped[date]
    account_type: Mapped[AccountType]
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    paid: Mapped[bool] = mapped_column(default=False)

    user: Mapped['User'] = relationship(
        back_populates='accounts', lazy='immediate', init=False
    )
