from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from dotum.utils.enum import AccountType

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    user: Mapped['Account'] = relationship(
        back_populates='users', lazy='immediate', init=False
    )


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'

    value: Mapped[float]
    description: Mapped[str]
    due_date: Mapped[date]
    account_type: Mapped[AccountType]
    paid: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    user: Mapped['User'] = relationship(
        back_populates='accounts', lazy='immediate', init=False
    )
