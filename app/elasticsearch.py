import requests
from utils import raise_for_status
from config import ELASTIC_URL, ELASTIC_USERNAME, ELASTIC_PASSWORD
from log import logger

CACHE = {}

def get_manifest_for_zip(media_id):
    return __get_media(media_id)['_source']['metadata']['elearning_manifest']

def update_media_id_for_module(course_id, module_id, media_id):
    logger.info(f"Setting media ID {media_id}")
    course = __get_course(course_id)
    for mod in course['modules']:
        if mod['id'] == module_id:
            mod['mediaId'] = media_id
            __save_course(course_id, course)
            return
    raise Exception(f"Module not found for course ID: '{course_id}' and module ID: '{module_id}'")

def update_media_id_for_module_and_get_existing(course_id, module_id, media_id):
    logger.info(f"Setting media ID {media_id}")
    course = __get_course(course_id)
    existing_media_id = None
    for mod in course['modules']:
        if mod['id'] == module_id:
            existing_media_id = mod.get('mediaId', None)
            mod['mediaId'] = media_id
            logger.info(f"Fetching existing media ID {existing_media_id}")
            __save_course(course_id, course)
            return existing_media_id
    raise Exception(f"Module not found for course ID: '{course_id}' and module ID: '{module_id}'")

def __get_course(course_id):
    logger.info(f"Getting course {course_id} from elastic search")
    course = CACHE.get(course_id)
    if not course:
        course_resp = requests.request("GET", url=f"{ELASTIC_URL}/courses/_doc/{course_id}", auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD))
        raise_for_status(course_resp)
        course = course_resp.json()['_source']
        CACHE[course_id] = course
    return course

def __save_course(course_id, course):
    CACHE[course_id] = course
    updated_doc = {'doc': course}
    requests.request("POST", url=f"{ELASTIC_URL}/courses/_update/{course_id}", json=updated_doc, auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)).raise_for_status()

def __get_media(media_id):
    resp = requests.request("GET", url=f"{ELASTIC_URL}/media/_doc/{media_id}", auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD))
    raise_for_status(resp)
    return resp.json()