from fastapi import status

from dotum.core.security import create_access_token


def test_get_token(client, user):
    response = client.post(
        '/token', data={'username': user.username, 'password': 'testtest'}
    )
    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_not_user(client):
    response = client.post(
        '/token', data={'username': 'testusername', 'password': 'testtest'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_get_token_not_verify_password(client, user):
    response = client.post(
        '/token', data={'username': user.username, 'password': 'passworderror'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_refresh_token_success(client, user):
    access_token = create_access_token(data={'sub': user.username})

    response = client.post(
        '/refresh_token', headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200
    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
