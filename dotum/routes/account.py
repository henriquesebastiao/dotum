from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from dotum.core.database import get_session
from dotum.models import Account
from dotum.schemas import Message
from dotum.schemas.account import AccountCreate, AccountSchema, AccountUpdate
from dotum.utils import response
from dotum.utils.database import upattr
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
