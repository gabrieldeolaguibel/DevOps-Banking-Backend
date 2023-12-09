from iebank_api import app
import pytest


def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get("/accounts")
    assert response.status_code == 200


def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get("/wrong_path")
        assert response.status_code == 404


def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )
    assert response.status_code == 200


# write a function that tests update account
def test_change_account_name(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (PUT) with an name
    THEN check the response is valid
    """
    testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )
    response = testing_client.put(
        "/accounts/0580982293", json={"name": "Keti", "account_number": "0580982293"}
    )
    assert response.status_code == 200


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page posted to delete (DELETE)
    THEN check the response is valid
    """

    # Create an account first
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Delete the account by id
    response = testing_client.delete(
        "/accounts/0580982293", json={"account_number": "0580982293"}
    )
    assert response.status_code == 200


def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
        },
    )

    # Get the account by id
    response = testing_client.get("/accounts/customer/1")
    assert response.status_code == 200


def test_deposit(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/deposit' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Deposit into the account
    response = testing_client.put(
        "/accounts/1/deposit",
        json={"account_number": "0580982293", "deposit": 1000},
    )
    print(response.data)
    assert response.status_code == 200


def test_withdraw_from_balance(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/withdraw' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Deposit into the account
    response = testing_client.put(
        "/accounts/1/deposit",
        json={"account_number": "0580982293", "deposit": 1000},
    )

    # Withdraw from the account
    response = testing_client.put(
        "/accounts/1/withdraw",
        json={"account_number": "0580982293", "withdraw": 100},
    )
    print(response.data)
    assert response.status_code == 200


def test_withdraw_fail(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/withdraw' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Withdraw from the account
    response = testing_client.put(
        "/accounts/1/withdraw",
        json={"account_number": "0580982293", "withdraw": 10000},
    )
    assert response.status_code == 400


def test_transfer_money(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/transfer' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Create another account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 2,
            "name": "Keti",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982294",
        },
    )

    # Deposit into the account
    response = testing_client.put(
        "/accounts/1/deposit",
        json={"account_number": "0580982293", "deposit": 1000},
    )

    # Transfer money from one account to another
    response = testing_client.put(
        "/accounts/1/transfer",
        json={
            "account_number1": "0580982293",
            "account_number2": "0580982294",
            "amount": 100,
        },
    )
    assert response.status_code == 200


def test_transfer_money_invalid_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/transfer' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Create another account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 2,
            "name": "Keti",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982294",
        },
    )

    # Deposit into the account
    response = testing_client.put(
        "/accounts/1/deposit",
        json={"account_number": "0580982293", "deposit": 1000},
    )

    # Transfer money from one account to another
    response = testing_client.put(
        "/accounts/1/transfer",
        json={
            "account_number1": "0580982293",
            "account_number2": "0580982295",
            "amount": 100,
        },
    )
    assert response.status_code == 404


def test_transfer_money_insufficient_balance(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>/transfer' page is requested (PUT)
    THEN check the response is valid
    """

    # Create an account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 1,
            "name": "John Doe",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982293",
        },
    )

    # Create another account
    response = testing_client.post(
        "/accounts",
        json={
            "id": 2,
            "name": "Keti",
            "password": "Password",
            "country": "Spain",
            "currency": "€",
            "account_number": "0580982294",
        },
    )

    # Deposit into the account
    response = testing_client.put(
        "/accounts/1/deposit",
        json={"account_number": "0580982293", "deposit": 1000},
    )

    # Transfer money from one account to another
    response = testing_client.put(
        "/accounts/1/transfer",
        json={
            "account_number1": "0580982293",
            "account_number2": "0580982294",
            "amount": 10000,
        },
    )
    assert response.status_code == 400
