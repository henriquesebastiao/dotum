from datetime import date

from fastapi import status


def test_create_account(client, user, auth):
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
        headers=auth,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = response.json()

    assert response['value'] == 1500
    assert response['description'] == 'Test account'
    assert response['due_date'] == due_date
    assert response['account_type'] == 'payable'
    assert not response['paid']
    assert response['created_by'] == user.id


def test_update_account(client, account, auth):
    response = client.patch(
        f'/account/{account.id}',
        json={
            'value': 2000,
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['value'] == 2000


def test_update_account_does_not_exists(client, auth):
    response = client.patch(
        '/account/1000',
        json={
            'value': 2000,
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account does not exist'}


def test_update_account_of_other_user(client, auth, account2):
    response = client.patch(
        f'/account/{account2.id}',
        json={
            'value': 2000,
        },
        headers=auth,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_account(client, account, auth):
    response = client.delete(f'/account/{account.id}', headers=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Conta deletada'}


def test_delete_account_of_other_user(client, account2, auth):
    response = client.delete(f'/account/{account2.id}', headers=auth)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_account_does_not_exist(client, auth):
    response = client.delete('/account/1', headers=auth)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account does not exist'}


def test_get_all_accounts(client, account, auth):
    response = client.get('/account/', headers=auth)

    assert response.status_code == status.HTTP_200_OK

    response = response.json()

    assert response == {
        'accounts': [
            {
                'value': 1500,
                'description': 'Test account',
                'due_date': date.today().isoformat(),
                'account_type': 'payable',
                'paid': False,
            }
        ]
    }


def test_get_total_accounts_payable(
    client, account_payable_2000, account_payable_2500, auth
):
    response = client.get('/account/total-accounts-payable/', headers=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['total'] == 4500


def test_get_total_accounts_receivable(
    client, account_receivable_1200, account_receivable_1300, auth
):
    response = client.get('/account/total-accounts-receivable/', headers=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['total'] == 2500


def test_get_grand_total_of_accounts(
    client, account_payable_2000, account_receivable_1200, auth
):
    response = client.get('/account/grand-total-of-accounts/', headers=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['total'] == -800
