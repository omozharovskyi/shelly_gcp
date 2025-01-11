import json
import logging
import boto3
from google.cloud import storage
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_gcp_access_secret():
    secret_name = "GCPTransferJobAccessTokenSecret"
    region_name = "eu-central-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as exception_error:
        logger.error(f"Error retrieving secret: {exception_error}")
        return None
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            logger.info(f"Retrieved GCP Access secret: {secret}")
            return json.loads(secret)
        else:
            logger.error("Secret does not contain 'SecretString'")
            return None

def lambda_handler(event, context):
    logger.info("Start of the function")
    gcp_credentials = service_account.Credentials.from_service_account_info(get_gcp_access_secret())
    logger.info(f'Retrived credentials: {gcp_credentials}')
    aws_s3bucket_name = event.get('s3bucket')
    filenames = event.get('filenames', [])
    gcp_bucket_name = 'mozharovskyi-shelly-gcp-agregated-mqtt-storage-eu'
    s3_client = boto3.client('s3')
    gcp_storage_client = storage.Client(credentials=gcp_credentials)
    logger.info("GCP Storage Client created successfully")
    bucket = gcp_storage_client.bucket(gcp_bucket_name)
    for filename in filenames:
        # Read file from S3
        try:
            file_obj = s3_client.get_object(Bucket=aws_s3bucket_name, Key=filename)
            file_content = file_obj['Body'].read()
        except Exception as s3bucket_exception:
            logger.error(f"Failed to read file from S3: {s3bucket_exception}")
            continue  # Skip this file and continue with the next
        # Upload file to GCP
        blob = bucket.blob(filename)
        try:
            blob.upload_from_string(file_content)
        except Exception as gcpbucket_exception:
            logger.error(f"Failed to upload file to GCP: {gcpbucket_exception}")
            continue  # Skip this file and continue with the next
        logger.info(f"File {filename} successfully transferred to GCP")
    logger.info("End of the function")
    return {
        'statusCode': 200,
        'body': json.dumps("Files processing completed")
    }