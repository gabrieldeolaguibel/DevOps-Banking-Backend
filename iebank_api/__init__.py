from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from applicationinsights.flask.ext import AppInsights

app = Flask(__name__)

load_dotenv()

# Select environment based on the ENV environment variable
if os.getenv("ENV") == "local":
    print("Running in local mode")
    app.config.from_object("config.LocalConfig")
elif os.getenv("ENV") == "dev":
    print("Running in development mode")
    app.config.from_object("config.DevelopmentConfig")
elif os.getenv("ENV") == "ghci":
    print("Running in github mode")
    app.config.from_object("config.GithubCIConfig")
elif os.getenv("ENV") == "uat":
    print("Running in UAT mode")
    app.config.from_object("config.UATConfig")
else:
    print("Running in production mode")
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)

from iebank_api.models import Account

with app.app_context():
    db.create_all()
CORS(app)

from iebank_api import routes

# Initialize Application Insights and force flushing application insights handler after each request
if os.getenv("ENV") == "dev" or os.getenv("ENV") == "uat":
    appinsights = AppInsights(app)

    @app.after_request
    def after_request(response):
        appinsights.flush()
        return response
