from flask import Flask, request
from iebank_api import db, app
from iebank_api.models import Account


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
def create_account():
    id = request.json["id"]
    name = request.json["name"]
    password = request.json["password"]
    country = request.json["country"]
    currency = request.json["currency"]
    account = Account(id, name, password, country, currency)
    db.session.add(account)
    db.session.commit()
    return format_account(account)


@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()
    return {"accounts": [format_account(account) for account in accounts]}


@app.route("/auth/<string:name>:<string:password>", methods=["GET"])
def check_credentials(name, password):
    account = Account.query.filter_by(name=name, password=password).first()
    if account is None:
        return {}
    else:
        return {"id": account.id, "name": account.name, "password": account.password}


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
        account.password = request.json["password"]
    db.session.commit()
    return get_accounts_by_id(id)


# Route to transfer money between accounts
@app.route(
    "/accounts/transfer/<int:account_number1>:<int:account_number2>:amount",
    methods=["PUT"],
)
def transfer(account_number1, account_number2, amount):
    from_account = Account.query.get(account_number1)
    to_account = Account.query.get(account_number2)
    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        db.session.commit()
        return {"status": "OK"}
    else:
        return {"status": "Not enough balance"}


# Update an account name by its account number
@app.route("/accounts/<int:account_number>", methods=["PUT"])
def update_account_by_number(account_number):
    account = Account.query.get(account_number)
    account.name = request.json["name"]
    db.session.commit()
    return format_account(account)


# Delete an account by its account number
@app.route("/accounts/<int:account_number>", methods=["DELETE"])
def delete_account_by_number(account_number):
    account = Account.query.get(account_number)
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
