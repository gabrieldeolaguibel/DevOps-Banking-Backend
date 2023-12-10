# iebank_api/services.py or iebank_api/business_logic.py
from iebank_api import db
from iebank_api.models import Account


def create_account(id, name, password, country, currency, account_number=None):
    password = encrypt_password(password)  # Encrypt password
    if get_accounts_by_id(id) != {"accounts": []}:  # Check if ID exists
        password = get_accounts_by_id(id)["accounts"][0]["password"]
    account = Account(id, name, password, country, currency, account_number)
    db.session.add(account)
    db.session.commit()
    return format_account(account)


def format_account(account):
    return {
        "id": account.id,
        "name": account.name,
        "password": account.password,
        "country": account.country,
        "account_number": account.account_number,
        "balance": account.balance,
        "currency": account.currency,
        "status": account.status,
        "created_at": account.created_at,
    }


def encrypt_password(password):
    # Simple Ceasar cipher
    encrypted_password = ""
    for char in password:
        encrypted_password += chr(ord(char) + 1)
    return encrypted_password


def decrypt_password(password):
    # Simple Ceasar cipher
    decrypted_password = ""
    for char in password:
        decrypted_password += chr(ord(char) - 1)
    return decrypted_password


def get_accounts():
    accounts = Account.query.all()
    return {"accounts": [format_account(account) for account in accounts]}


def get_accounts_by_id(id):
    accounts = Account.query.filter_by(id=id).all()
    return {"accounts": [format_account(account) for account in accounts]}
