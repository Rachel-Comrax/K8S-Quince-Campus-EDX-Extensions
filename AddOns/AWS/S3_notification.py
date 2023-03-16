import boto3
import json
import jsonschema
from django.conf import settings
from django.core.cache import cache
import logging
log = logging.getLogger(__name__)


def get_json_file_from_s3(portal_name):
    """Get JSON file from AWS S3 bucket if exists, else return None.
    :param portal_name: Type of site (cms or lms)
    :return: JSON value from S3 JSON bucket
    """
    session = boto3.Session (
    aws_access_key_id = str(settings.AWS_ACCESS_KEY_ID),
    aws_secret_access_key = str(settings.AWS_SECRET_ACCESS_KEY)
    )
    bucket_name = str(settings.AWS_S3_POPUP_NOTIFICATIONS)
    file_name = str(portal_name)+str(settings.AWS_S3_ENV_NOTIFICATIONS)
    s3 = session.resource('s3')
    try:
        obj = s3.Object(bucket_name, file_name)
        file_content = obj.get()['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)
        is_valid = is_json_valid(json_data)
        if is_valid:
            json_data = str(json.loads(file_content)).replace("'",'"') 
            store_data_in_cache(portal_name, json_data)
            return str(json_data)
        else:
            log.error(f"From get_json_file_from_s3(portal_name): The JSON contain HTML/JS, please change it in order to see the popup notification you created")
            return None
    except:
        log.error(f"From get_json_file_from_s3(portal_name): The file name format is incorrect, please change it in order to see the popup notification you created")
        return None


def get_notification_data(portal_name):
    """Get Json file from cache or S3.
    :param portal_name: Type of site (cms or lms)
    :return: JSON file
    """
    data = get_data_from_cache(portal_name)
    if not data or data == 'None':
        data = get_json_file_from_s3(portal_name)
    return data
 

def get_data_from_cache(portal_name):
    """Get Json file from cache.
    :param portal_name: Type of site (cms or lms)
    :return: JSON file from cache
    """
    cache_key = settings.AWS_CACHE_POPUP_NOTIFICATIONS
    cache_key = portal_name + "-" + cache_key
    json_data = cache.get(cache_key)
    return json_data 
        
    
def store_data_in_cache(portal_name, json_data):
    """Store Json file in cache.
    :param portal_name: Type of site (cms or lms)
    :param json_data: JSON value from S3 JSON bucket
    """
    cache_key = settings.AWS_CACHE_POPUP_NOTIFICATIONS
    cache_key = portal_name + "-" + cache_key
    cache_time = settings.AWS_CACHE_TIME_IN_SEC
    cache.set(cache_key, json_data, cache_time)
    return str(json_data)

def is_json_valid(json_data):
    """Get Json file from cache.
    :param json_data: JSON value from S3 JSON bucket
    :return: True if JSON is valid, else if not.
    """
    schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "string",
            "pattern": "^[^<>&]*$"
            }
        }
    }
    try:
        jsonschema.validate(json_data, schema)
        return True
    except:
        return False
