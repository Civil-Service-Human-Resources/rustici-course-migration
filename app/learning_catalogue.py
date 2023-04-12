import requests
from config import LEARNING_CATALOGUE_URL
from identity import get_token
from utils import raise_for_status
from log import logger

def upload_file(course_id, file):
    token_data = get_token()

    url = f"{LEARNING_CATALOGUE_URL}/media?container={course_id}"
    # File data should be in bytes
    file_payload = [('file', (file.filename, file.data, 'application/zip'))]
    headers = {
        'Authorization': f'Bearer {token_data}'
    }
    logger.info(f"Uploading file to catalogue")
    resp = requests.request("POST", url, headers=headers, files=file_payload)
    raise_for_status(resp)
    media_location = resp.headers['Location']
    logger.info(f"Resulting media location: {media_location}")
    return media_location.split("/")[-1]