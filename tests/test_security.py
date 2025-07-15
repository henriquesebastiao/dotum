from jwt import decode

from dotum.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from dotum.core.settings import get_settings

settings = get_settings()


def test_jwt():
    data = {'sub': 'user@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']  # Testa se o valor de exp foi adicionado ao token


def test_verify_password():
    plain_text = 'password'
    pwd_hash = get_password_hash(plain_text)

    assert verify_password(plain_text, pwd_hash)
