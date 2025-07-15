from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from dotum.core.database import get_session
from dotum.core.security import get_password_hash
from dotum.main import app
from dotum.models import Account, User, table_registry


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17-alpine', driver='psycopg') as postgres:
        yield create_engine(postgres.get_connection_url())


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(
        username='test',
        email='test@test.com',
        password=get_password_hash('testtest'),
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


@pytest.fixture
def account2(session, user2):
    account = Account(
        value=1500,
        description='Test account',
        due_date=datetime.now(),
        account_type='payable',
        paid=False,
        created_by=user2.id,
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@pytest.fixture
def account_payable_2000(session, user):
    account = Account(
        value=2000,
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


@pytest.fixture
def account_payable_2500(session, user):
    account = Account(
        value=2500,
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


@pytest.fixture
def account_receivable_1200(session, user):
    account = Account(
        value=1200,
        description='Test account',
        due_date=datetime.now(),
        account_type='receivable',
        paid=False,
        created_by=user.id,
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@pytest.fixture
def account_receivable_1300(session, user):
    account = Account(
        value=1300,
        description='Test account',
        due_date=datetime.now(),
        account_type='receivable',
        paid=False,
        created_by=user.id,
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': 'testtest'},
    )

    return response.json()['access_token']


@pytest.fixture
def auth(token):
    return {'Authorization': f'Bearer {token}'}
