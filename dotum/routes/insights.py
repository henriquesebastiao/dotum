from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from dotum.core.database import get_session
from dotum.core.security import get_current_user
from dotum.models import Account, User
from dotum.schemas.account import TotalAccounts
from dotum.utils.enum import AccountType

router = APIRouter(prefix='/insights', tags=['Insights'])


@router.get(
    '/total-accounts-payable',
    response_model=TotalAccounts,
    summary='Retorna o total de contas a pagar',
)
def get_total_accounts_payable(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    stmt = select(func.sum(Account.value)).where(
        (Account.account_type == AccountType.PAYABLE) & (Account.paid == False)
    )
    total = session.execute(stmt).scalar_one_or_none() or 0.0

    return {'total': total}


@router.get(
    '/total-accounts-receivable',
    response_model=TotalAccounts,
    summary='Retorna o total de contas a receber',
)
def get_total_accounts_receivable(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    stmt = select(func.sum(Account.value)).where(
        (Account.account_type == AccountType.RECEIVABLE)
        & (Account.paid == False)
    )
    total = session.execute(stmt).scalar_one_or_none() or 0.0

    return {'total': total}


@router.get(
    '/grand-total-of-accounts',
    response_model=TotalAccounts,
    summary='Retorna o total geral de contas',
)
def get_grand_total_of_accounts(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    def get_total(account_type: AccountType) -> float:
        stmt = select(func.sum(Account.value)).where(
            (Account.account_type == account_type) & (Account.paid == False)
        )
        return session.execute(stmt).scalar() or 0.0

    receivable = get_total(AccountType.RECEIVABLE)
    payable = get_total(AccountType.PAYABLE)

    grand_total = receivable - payable

    return {'total': grand_total}
