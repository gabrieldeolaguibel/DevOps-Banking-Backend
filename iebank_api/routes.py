from flask import Flask, request, jsonify
from iebank_api import db, app
from iebank_api.models import Account

import iebank_api.services as services


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/skull", methods=["GET"])
def skull():
    text = "Hi! This is the BACKEND SKULL! 💀 "

    text = text + "<br/>Database URL:" + db.engine.url.database
    if db.engine.url.host:
        text = text + "<br/>Database host:" + db.engine.url.host
    if db.engine.url.port:
        text = text + "<br/>Database port:" + db.engine.url.port
    if db.engine.url.username:
        text = text + "<br/>Database user:" + db.engine.url.username
    if db.engine.url.password:
        text = text + "<br/>Database password:" + db.engine.url.password
    return text


@app.route("/accounts", methods=["POST"])
def create_account_route():
    id = request.json["id"]
    name = request.json["name"]
    password = request.json["password"]
    country = request.json["country"]
    currency = request.json["currency"]
    account_number = None
    if "account_number" in request.json:
        account_number = request.json["account_number"]
    return services.create_account(
        id, name, password, country, currency, account_number
    )


@app.route("/accounts", methods=["GET"])
def get_accounts():
    return services.get_accounts()


@app.route("/auth/<string:name>:<string:password>", methods=["GET"])
def check_credentials(name, password):
    account = Account.query.filter_by(
        name=name, password=encrypt_password(password)
    ).first()
    if account is None:
        return {}
    else:
        return {"id": account.id, "name": account.name, "password": account.password}


@app.route("/accounts/<string:account_number>", methods=["PUT"])
def change_account_name(account_number):
    return services.change_account_name(account_number, request.json["name"])


# New get account route (ID not primary key, it's the account number)
@app.route("/accounts/<int:account_number>", methods=["GET"])
def get_account_by_number(account_number):
    account = Account.query.get(account_number)
    return format_account(account)


# Route to fetch all accounts by customer ID
@app.route("/accounts/customer/<int:id>", methods=["GET"])
def get_accounts_by_id(id):
    accounts = Account.query.filter_by(id=id)
    return {"accounts": [format_account(account) for account in accounts]}


# Route to change password in an account given its ID
@app.route("/accounts/<int:id>/change_password", methods=["PUT"])
def change_password(id):
    accounts = Account.query.filter_by(id=id).all()
    for account in accounts:
        account.password = encrypt_password(request.json["password"])
    db.session.commit()
    return get_accounts_by_id(id)


@app.route("/accounts/<int:id>/deposit", methods=["PUT"])
def deposit(id):
    return services.deposit(request.json["account_number"], request.json["deposit"])


@app.route("/accounts/<int:id>/withdraw", methods=["PUT"])
def withdraw(id):
    return services.withdraw(request.json["account_number"], request.json["withdraw"])


# Route to transfer money between accounts
@app.route("/accounts/<int:id>/transfer", methods=["PUT"])
def transfer_money(id):
    account_from = Account.query.get(request.json["account_number1"])
    account_to = Account.query.get(request.json["account_number2"])
    if not account_from or not account_to:
        return jsonify({"error": "Account does not exist"}), 404
    if float(account_from.balance) < float(request.json["amount"]):
        return jsonify({"error": "Insufficient balance"}), 400
    account_from.balance -= float(request.json["amount"])
    account_to.balance += float(request.json["amount"])

    db.session.commit()
    return get_accounts()


# Delete an account by its account number
@app.route("/accounts/<string:account_number>", methods=["DELETE"])
def delete_account_by_number(account_number):
    account = Account.query.get(str(account_number))
    db.session.delete(account)
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
