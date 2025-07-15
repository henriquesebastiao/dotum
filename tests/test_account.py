from datetime import date

from fastapi import status


def test_create_account(client, user):
    due_date = date.today().isoformat()

    response = client.post(
        '/account',
        json={
            'value': 1500,
            'description': 'Test account',
            'due_date': date.today().isoformat(),
            'account_type': 'payable',
            'paid': False,
            'created_by': user.id,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = response.json()

    assert response['value'] == 1500
    assert response['description'] == 'Test account'
    assert response['due_date'] == due_date
    assert response['account_type'] == 'payable'
    assert not response['paid']
    assert response['created_by'] == user.id


def test_update_account(client, account):
    response = client.patch(
        f'/account/{account.id}',
        json={
            'value': 2000,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['value'] == 2000


def test_update_account_does_not_exists(client):
    response = client.patch(
        '/account/1',
        json={
            'value': 2000,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account does not exist'}


def test_delete_account(client, account):
    response = client.delete(f'/account/{account.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Conta deletada'}


def test_delete_account_does_not_exist(client):
    response = client.delete('/account/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account does not exist'}
