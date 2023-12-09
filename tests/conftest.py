import pytest
from iebank_api.models import Account
from iebank_api import db, app


@pytest.fixture
def testing_client(scope="module"):
    with app.app_context():
        db.create_all()
        account = Account(1, "John Doe", "password", "Spain", "€", None)
        db.session.add(account)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()
