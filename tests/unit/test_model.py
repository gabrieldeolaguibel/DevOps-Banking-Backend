from iebank_api.models import Account
import pytest


def test_account_create():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account("John Doe", "Spain", "€")
    assert account.name == "John Doe"
    assert account.country == "Spain"
    assert account.currency == "€"
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == "Active"


def test_account_repr():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the __repr__ method is defined correctly
    """
    account = Account("John Doe", "Spain", "€")
    assert repr(account) == f"<Event '{(account.account_number)}'>"


def test_account_deactivate():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the __deactivate__ method is defined correctly
    """
    account = Account("John Doe", "Spain", "€")
    assert account.__deactivate__() == "Inactive"
