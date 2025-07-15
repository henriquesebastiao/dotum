from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from dotum.core.database import get_session
from dotum.models import Account
from dotum.schemas import Message
from dotum.schemas.account import (
    AccountCreate,
    AccountList,
    AccountSchema,
    AccountUpdate,
    TotalAccounts,
)
from dotum.utils import response
from dotum.utils.database import upattr
from dotum.utils.enum import AccountType
from dotum.utils.message import DoesNotExist

router = APIRouter(prefix='/account', tags=['Contas'])


@router.post(
    '/',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Registra uma nova conta',
)
def create_account(
    schema: AccountCreate, session: Session = Depends(get_session)
):
    db_user = Account(**schema.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.patch(
    '/{account_id}',
    response_model=AccountSchema,
    responses=response.CHANGE_ACCOUNT,
    summary='Atualiza uma conta',
)
def update_account(
    account_id: int,
    schema: AccountUpdate,
    session: Session = Depends(get_session),
):
    db_account = session.scalar(
        select(Account).where(Account.id == account_id)
    )

    if db_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=DoesNotExist.ACCOUNT,
        )

    upattr(schema, db_account)

    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    return db_account


@router.delete(
    '/{account_id}',
    response_model=Message,
    responses=response.CHANGE_ACCOUNT,
    summary='Deleta uma conta',
)
def delete_account(account_id: int, session: Session = Depends(get_session)):
    db_account = session.scalar(
        select(Account).where(Account.id == account_id)
    )

    if db_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=DoesNotExist.ACCOUNT,
        )

    session.delete(db_account)
    session.commit()

    return {'message': 'Conta deletada'}


@router.get(
    '/',
    response_model=AccountList,
    summary='Retorna uma lista com todas as contas e seus dados',
)
def get_all_accounts(session: Session = Depends(get_session)):
    stmt = select(
        Account.value,
        Account.description,
        Account.due_date,
        Account.account_type,
        Account.paid,
    )
    accounts = session.execute(stmt).mappings().all()

    return {'accounts': accounts}


@router.get(
    '/total-accounts-payable',
    response_model=TotalAccounts,
    summary='Retorna o total de contas a pagar',
)
def get_total_accounts_payable(session: Session = Depends(get_session)):
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
def get_total_accounts_receivable(session: Session = Depends(get_session)):
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
def get_grand_total_of_accounts(session: Session = Depends(get_session)):
    def get_total(account_type: AccountType) -> float:
        stmt = select(func.sum(Account.value)).where(
            (Account.account_type == account_type) & (Account.paid == False)
        )
        return session.execute(stmt).scalar() or 0.0

    receivable = get_total(AccountType.RECEIVABLE)
    payable = get_total(AccountType.PAYABLE)

    grand_total = receivable - payable

    return {'total': grand_total}
