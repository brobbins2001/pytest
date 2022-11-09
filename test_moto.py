import os
import pytest
import logging
import boto3
from botocore.exceptions import ClientError
from moto import mock_s3

# test bucket specific to class and person
TEST_BUCKET = "comp630-m1-f21-proftim"
TEST_FILE = "btr1014.moto"


def to_the_cloud(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.Session(profile_name='default').client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f'Upload Response: {response}')
    except ClientError as e:
        logging.error(e)
        return False

    return True


@mock_s3
def test_upload():
    # make scope global
    global TEST_BUCKET
    global TEST_FILE
    # With the moto library imported, the boto3 s3 is fake
    conn = boto3.client("s3", region_name="us-east-1")
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket=TEST_BUCKET)
    with open(TEST_FILE, "rb") as f:
        object_name = os.path.basename(f.name)
        to_the_cloud(f.name, TEST_BUCKET, TEST_FILE)

    assert True


