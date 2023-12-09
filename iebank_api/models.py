from iebank_api import db
from datetime import datetime
import string
import random


class Account(db.Model):
    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    account_number = db.Column(
        db.String(10), nullable=False, unique=True, primary_key=True
    )
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return "<Event %r>" % self.id

    def __deactivate__(self):
        self.status = "Inactive"
        return self.status

    def __init__(self, id, name, password, country, currency, account_number):
        self.id = id
        self.name = name
        self.password = password
        self.country = country
        if account_number == None:
            self.account_number = "".join(random.choices(string.digits, k=10))
        else:
            self.account_number = account_number
        self.currency = currency
        self.balance = 0.0
        self.status = "Active"
