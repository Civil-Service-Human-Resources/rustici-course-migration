from dotenv import load_dotenv
from log import logger
import os

load_dotenv()

BLOB_LOGGING_DISABLED=os.getenv('BLOB_LOGGING_DISABLED', True)

ELEARNING_BLOB_CONNECTION_STRING=os.getenv('ELEARNING_BLOB_CONNECTION_STRING')
ELEARNING_BLOB_CONTAINER=os.getenv('ELEARNING_BLOB_CONTAINER', 'e-learning')

ZIP_BLOB_CONNECTION_STRING=os.getenv('ZIP_BLOB_CONNECTION_STRING')
ZIP_BLOB_CONTAINER=os.getenv('ZIP_BLOB_CONTAINER', 'zips')

ELASTIC_URL=os.getenv('ELASTIC_URL')
ELASTIC_USERNAME=os.getenv('ELASTIC_USERNAME')
ELASTIC_PASSWORD=os.getenv('ELASTIC_PASSWORD')

RUSTICI_SERVER_URL=os.getenv('RUSTICI_SERVER_URL')
RUSTICI_USERNAME=os.getenv('RUSTICI_USERNAME')
RUSTICI_PASSWORD=os.getenv('RUSTICI_PASSWORD')
RUSTICI_TENTANT=os.getenv('RUSTICI_TENANT')

LEARNING_CATALOGUE_URL=os.getenv('LEARNING_CATALOGUE_URL')

IDENTITY_URL=os.getenv('IDENTITY_URL')
TOKEN_USER=os.getenv('TOKEN_USER')
TOKEN_PASS=os.getenv('TOKEN_PASS')

__DATABASE_SERVER=os.getenv('DATABASE_SERVER')
__DATABASE_USER=os.getenv('DATABASE_USER')
__DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
__DATABASE=os.getenv('DATABASE')

LOG_DB_TRANSACTIONS=os.getenv('LOG_DB_TRANSACTIONS', False)

def get_database_connection():
    if __DATABASE_SERVER and __DATABASE_USER and __DATABASE_PASSWORD and __DATABASE:
        logger.info("Getting database credentials")
        return f"mysql://{__DATABASE_USER}:{__DATABASE_PASSWORD}@{__DATABASE_SERVER}/{__DATABASE}?ssl=true"
    else:
        logger.info("Getting database credentials for in-memory database")
        return "mysql:///:memory:"