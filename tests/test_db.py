from sqlalchemy import select
from sqlalchemy.orm import Session

from dotum.core.database import get_session
from dotum.models import User


def test_create_user(session):
    new_user = User(
        username='joao',
        password='secret',
        email='teste@test.com',
        first_name='João',
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'joao'))

    assert user.username == 'joao'


def test_get_session_returns_session():
    gen = get_session()

    session = next(gen)

    assert isinstance(session, Session)
    assert session.is_active

    try:
        next(gen)
    except StopIteration:
        pass
