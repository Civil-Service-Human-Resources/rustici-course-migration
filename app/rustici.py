from config import RUSTICI_SERVER_URL, RUSTICI_USERNAME, RUSTICI_PASSWORD, RUSTICI_TENTANT
import requests
from utils import raise_for_status
from log import logger

RUSTICI_API_URL = f"{RUSTICI_SERVER_URL}/RusticiEngine/api/v2"
RUSTICI_CDN_URL = f"{RUSTICI_SERVER_URL}/cdn"

def upload_course(course_id, module_id, media_id, manifest_filename):
    rustici_course_id = f"{course_id}.{module_id}"
    url = f"{RUSTICI_API_URL}/courses?courseId={course_id}.{module_id}"
    data = {
        "referenceRequest": {
            "webPathToCourse": f"{RUSTICI_CDN_URL}/{course_id}/{media_id}",
            "url": f"{RUSTICI_CDN_URL}/{course_id}/{media_id}/{manifest_filename}"
        }
    }
    resp = requests.request("POST", url=url, headers={"engineTenantName": RUSTICI_TENTANT}, auth=(RUSTICI_USERNAME, RUSTICI_PASSWORD), json=data)
    try:
        raise_for_status(resp)
    except Exception as e:
        if "course already exists" in resp.text:
            logger.info(f"Rustici course '{rustici_course_id}' already exists. Deleting and reuploading.")
            delete_course(course_id, module_id)
            return upload_course(course_id, module_id, media_id, manifest_filename)
        else:
            raise e
    return rustici_course_id

def delete_course(course_id, module_id):
    url = f"{RUSTICI_API_URL}/courses/{course_id}.{module_id}"
    resp = requests.request("DELETE", url=url, headers={"engineTenantName": RUSTICI_TENTANT}, auth=(RUSTICI_USERNAME, RUSTICI_PASSWORD))
    raise_for_status(resp)