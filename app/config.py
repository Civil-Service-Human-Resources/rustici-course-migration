from dotenv import load_dotenv
from log import logger
import os

load_dotenv()

BLOB_LOGGING_DISABLED=os.getenv('BLOB_LOGGING_DISABLED', True)

ELEARNING_BLOB_CONNECTION_STRING=os.environ['ELEARNING_BLOB_CONNECTION_STRING']
ELEARNING_BLOB_CONTAINER=os.getenv('ELEARNING_BLOB_CONTAINER', 'e-learning')

ZIP_BLOB_CONNECTION_STRING=os.environ['ZIP_BLOB_CONNECTION_STRING']
ZIP_BLOB_CONTAINER=os.getenv('ZIP_BLOB_CONTAINER', 'zips')

ELASTIC_URL=os.environ['ELASTIC_URL']
ELASTIC_USERNAME=os.environ['ELASTIC_USERNAME']
ELASTIC_PASSWORD=os.environ['ELASTIC_PASSWORD']

RUSTICI_SERVER_URL=os.environ['RUSTICI_SERVER_URL']
RUSTICI_USERNAME=os.environ['RUSTICI_USERNAME']
RUSTICI_PASSWORD=os.environ['RUSTICI_PASSWORD']
RUSTICI_TENTANT=os.environ['RUSTICI_TENANT']

LEARNING_CATALOGUE_URL=os.environ['LEARNING_CATALOGUE_URL']

IDENTITY_URL=os.environ['IDENTITY_URL']
TOKEN_USER=os.environ['TOKEN_USER']
TOKEN_PASS=os.environ['TOKEN_PASS']

__DATABASE_SERVER=os.environ['DATABASE_SERVER']
__DATABASE_USER=os.environ['DATABASE_USER']
__DATABASE_PASSWORD=os.environ['DATABASE_PASSWORD']
__DATABASE=os.environ['DATABASE']

LOG_DB_TRANSACTIONS=os.getenv('LOG_DB_TRANSACTIONS', False)

def get_database_connection():
    if __DATABASE_SERVER and __DATABASE_USER and __DATABASE_PASSWORD and __DATABASE:
        logger.info("Getting database credentials")
        return f"mysql://{__DATABASE_USER}:{__DATABASE_PASSWORD}@{__DATABASE_SERVER}/{__DATABASE}?ssl=true"
    else:
        logger.info("Getting database credentials for in-memory database")
        return "mysql:///:memory:"