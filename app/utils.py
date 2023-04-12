from log import logger
from requests import Response

def raise_for_status(resp: Response):
    try:
        resp.raise_for_status()
    except Exception as e:
        if resp.status_code >= 400:
            logger.error(f"Client error response data: {resp.text}")
        raise e