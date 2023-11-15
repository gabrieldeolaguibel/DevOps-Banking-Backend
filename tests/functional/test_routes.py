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
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )
    assert response.status_code == 200

# write a function that tests update account
def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (PUT) with an name
    THEN check the response is valid
    """
    testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )  
    response = testing_client.put("/accounts/1", json={"name": "Keti"})
    assert response.status_code == 200


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page posted to delete (DELETE)
    THEN check the response is valid
    """

    # Create an account first
    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )

    # Delete the account by id
    response = testing_client.delete("/accounts/1")
    assert response.status_code == 200


def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """

    # Create an account 
    response = testing_client.post(
        "/accounts", json={"name": "John Doe", "country": "Spain", "currency": "€"}
    )

    # Get the account by id
    response = testing_client.get("/accounts/1")
    assert response.status_code == 200
