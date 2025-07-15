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


def test_update_user(client, user):
    response = client.patch(
        f'/user/{user.id}',
        json={'email': 'testeupdate@test.com'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'testeupdate@test.com'


def test_update_user_already_exists_email(client, user):
    response = client.patch(
        f'/user/{user.id}',
        json={
            'email': 'test@test.com',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_update_user_already_exists_username(client, user):
    response = client.patch(
        f'/user/{user.id}',
        json={
            'username': 'test',
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_update_user_does_not_exists(client):
    response = client.patch(
        '/user/1',
        json={
            'username': 'test',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User does not exist'}


def test_delete_user(client, user):
    response = client.delete(f'/user/{user.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Usuário deletado'}


def test_delete_user_does_not_exist(client):
    response = client.delete('/user/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User does not exist'}
