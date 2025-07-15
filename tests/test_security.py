from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException, status
from jwt import decode, encode

from dotum.core.security import (
    create_access_token,
    get_current_active_user,
    get_current_user,
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


def test_jwt_invalid_token(client, user):
    response = client.delete(
        f'/user/{user.id}', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_verify_password():
    plain_text = 'password'
    pwd_hash = get_password_hash(plain_text)

    assert verify_password(plain_text, pwd_hash)


def test_get_current_user_valid_token(user, session):
    token = create_access_token(data={'sub': user.username})
    result = get_current_user(session=session, token=token)
    assert result.username == user.username


def test_get_current_user_invalid_signature_token(session):
    # Token com chave errada
    token = encode(
        {'sub': 'test'}, 'wrong_secret', algorithm=settings.ALGORITHM
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'Could not validate credentials'


def test_get_current_user_expired_token(session):
    expire = datetime.utcnow() - timedelta(minutes=5)  # tempo no passado
    token = encode(
        {'sub': 'test', 'exp': expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'Your token has expired'


def test_get_current_user_missing_sub(session):
    # Token sem "sub"
    token = create_access_token(data={'foo': 'bar'})

    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'Could not validate credentials'


def test_get_current_user_user_not_found(session):
    # Gera token com usuário que não existe
    token = create_access_token(data={'sub': 'nonexistent'})

    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'Could not validate credentials'


def test_get_current_active_user(user):
    # Simula a dependência get_current_user retornando um User
    result = get_current_active_user(current_user=user)
    assert result == user
