from fastapi import status


def test_create_user(client):
    response = client.post(
        '/user',
        json={
            'username': 'joao',
            'password': 'senha_segura',
            'email': 'test@gmail.com',
            'first_name': 'João',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = response.json()

    assert response['username'] == 'joao'
    assert response['email'] == 'test@gmail.com'
    assert response['first_name'] == 'João'


def test_create_user_already_exists_email(client, user):
    response = client.post(
        '/user',
        json={
            'username': 'test3',
            'password': 'senha_segura',
            'email': 'test@test.com',
            'first_name': 'João',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_already_exists_username(client, user):
    response = client.post(
        '/user',
        json={
            'username': 'test',
            'password': 'senha_segura',
            'email': 'test3@test.com',
            'first_name': 'João',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_update_user(client, user, auth):
    response = client.patch(
        f'/user/{user.id}',
        json={'email': 'testeupdate@test.com'},
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'testeupdate@test.com'


def test_update_other_user(client, user2, auth):
    response = client.patch(
        f'/user/{user2.id}',
        json={'email': 'testeupdate@test.com'},
        headers=auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user_already_exists_email(client, user, auth):
    response = client.patch(
        f'/user/{user.id}',
        json={
            'email': 'test@test.com',
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_update_user_already_exists_username(client, user, auth):
    response = client.patch(
        f'/user/{user.id}',
        json={
            'username': 'test',
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_delete_user(client, user, auth):
    response = client.delete(f'/user/{user.id}', headers=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Usuário deletado'}


def test_delete_other_user(client, auth):
    response = client.delete('/user/10', headers=auth)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
