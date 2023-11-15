from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, ".db", "local.db")
    DEBUG = True


class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    DEBUG = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
        dbuser=os.getenv("DBUSER"),
        dbpass=os.getenv("DBPASS"),
        dbhost=os.getenv("DBHOST"),
        dbname=os.getenv("DBNAME"),
    )
    DEBUG = True


class UATConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
        dbuser=os.getenv("DBUSER"),
        dbpass=os.getenv("DBPASS"),
        dbhost=os.getenv("DBHOST"),
        dbname=os.getenv("DBNAME"),
    )
    DEBUG = False
