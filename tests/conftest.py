from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from dotum.core.database import get_session
from dotum.main import app
from dotum.models import Account, User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(
        username='test',
        email='test@test.com',
        password='testtest',
        first_name='Teste',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def user2(session):
    user = User(
        username='test2',
        email='test2@test.com',
        password='testtest',
        first_name='Teste',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def account(session, user):
    account = Account(
        value=1500,
        description='Test account',
        due_date=datetime.now(),
        account_type='payable',
        paid=False,
        created_by=user.id,
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return account
