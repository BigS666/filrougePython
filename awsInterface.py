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
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:


        session = boto3.Session(profile_name='csloginstudent')
        s3 = session.resource('s3')
        try:
            #response = s3_client.upload_file(file_name, bucket, object_name)
            s3.meta.client.upload_file(file_name, bucket, name)
        except ClientError as e:
            logging.error(e)
            return False
    except ProfileNotFound as pfe:
        logging.error(pfe)
        s3 = boto3.client('s3')
        try:
            s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
    return True

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):

    try:
        session = boto3.Session(profile_name='csloginstudent')
        rekognition = session.client('rekognition', region)
        try:
            #response = s3_client.upload_file(file_name, bucket, object_name)
            response = rekognition.detect_labels(
                Image={
                        "S3Object": {
                            "Bucket": bucket,
                            "Name": key,
                        }
                    },
                MaxLabels=max_labels,
                MinConfidence=min_confidence,
            )
            return response['Labels']
        except ClientError as e:
            logging.error(e)
            return False
    except ProfileNotFound as pfe:
        logging.error(pfe)
        rekognition = boto3.client("rekognition", region)
        try:
            response = rekognition.detect_labels(
                Image={
                        "S3Object": {
                            "Bucket": bucket,
                            "Name": key,
                        }
                    },
                MaxLabels=max_labels,
                MinConfidence=min_confidence,
            )
            return response['Labels']
        except ClientError as e:
            logging.error(e)
            return False
    return False

