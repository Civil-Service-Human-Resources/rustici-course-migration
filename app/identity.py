import requests
from config import IDENTITY_URL, TOKEN_USER, TOKEN_PASS
from datetime import datetime, timedelta
from utils import raise_for_status
from log import logger

CACHE = {
    'token': None,
    'expires': None
}

def get_token():
    now = datetime.now()
    if not CACHE['token'] or CACHE['expires'] >= now:
        token_data = __fetch_token()
        CACHE['token'] = token_data['access_token']
        CACHE['expires'] = now + timedelta(seconds=token_data['expires_in'])
    return CACHE['token']

def __fetch_token():
    logger.info(f"Getting token from identity service")
    res = requests.request("POST", f"{IDENTITY_URL}/oauth/token", auth=(TOKEN_USER, TOKEN_PASS), data={'grant_type': 'client_credentials'})
    raise_for_status(res)
    return res.json()
