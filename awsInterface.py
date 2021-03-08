import logging
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import ProfileNotFound

def upload_file(file_name, bucket, name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    try:
        session = boto3.Session(profile_name='csloginstudent')
    except ProfileNotFound as pfe:
        logging.error(pfe)

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    #s3_client = boto3.client('s3')
    s3 = session.resource('s3')
    try:
        #response = s3_client.upload_file(file_name, bucket, object_name)
        s3.meta.client.upload_file(file_name, bucket, name)
    except ClientError as e:
        logging.error(e)
        return False
    return True