import boto3
import json
from django.conf import settings


def get_json_file_from_s3(portal_name):
    """Get JSON file from AWS S3 bucket.
      
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
    obj = s3.Object(bucket_name, file_name)
    file_content = obj.get()['Body'].read().decode('utf-8')
    json_data = str(json.loads(file_content)).replace("'",'"') 
    return str(json_data)