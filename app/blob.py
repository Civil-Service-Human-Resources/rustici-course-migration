from azure.storage.blob import ContainerClient
from config import ZIP_BLOB_CONNECTION_STRING, ZIP_BLOB_CONTAINER, ELEARNING_BLOB_CONNECTION_STRING, ELEARNING_BLOB_CONTAINER, BLOB_LOGGING_DISABLED
from models.ZipFile import ZipFile
from log import logger

import logging
blob_logger = logging.getLogger("blob")
blob_logger.disabled = BLOB_LOGGING_DISABLED

zip_service = ContainerClient.from_connection_string(ZIP_BLOB_CONNECTION_STRING, container_name=ZIP_BLOB_CONTAINER, logger=blob_logger)
elearning_service = ContainerClient.from_connection_string(ELEARNING_BLOB_CONNECTION_STRING, container_name=ELEARNING_BLOB_CONTAINER, logger=blob_logger)

blob_cache = {}

def does_zip_exist(zip_filename):
    logger.info(f"Checking zip {zip_filename} exists in blob storage")
    blob_list = blob_cache.get("blob_names", [])
    if not blob_list:
        blob_list = [zip_name for zip_name in zip_service.list_blob_names()]
        blob_cache["blob_names"] = blob_list
    return zip_filename in blob_list

def load_zip_file(zip_filename):
    _bytes = zip_service.download_blob(zip_filename).readall()
    return ZipFile(zip_filename, _bytes)

def delete_elearning(course_id, media_id):
    blobs = elearning_service.list_blobs(f"{course_id}/{media_id}")
    for blob in blobs:
        elearning_service.delete_blob(blob.name)