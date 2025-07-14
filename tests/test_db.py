from sqlalchemy import select

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
