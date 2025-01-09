import json
import logging
import datetime
import boto3
import requests

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Configuration data
    project_id = 'shelly-gcp-data-analytics'
    job_name = 'transferJobs/shelly-get-data-from-aws'  # This can be None if the job has not been created yet
    gcp_access_token = ''  # Retrieve the token from Secrets Manager or environment variable
    gcp_bucket_name = ''
    delete_after_transfer = False

    # Retrieve the list of filenames from the event
    filenames = event.get('filenames', [])
    aws_s3bucket_name = event.get('s3bucket')

    # Check if files exist in the S3 bucket and filter out non-existing files
    existing_filenames = []
    for filename in filenames:
        try:
            response = s3_client.head_object(Bucket=aws_s3bucket_name, Key=filename)
            existing_filenames.append(filename)
        except s3_client.exceptions.ClientError as defined_error:
            if defined_error.response['Error']['Code'] == '404':
                logger.info(f"File {filename} does not exist.")
            else:
                logger.info(f'Unexpected error: {defined_error}')
    logger.info(f"Files to transfer: {existing_filenames}")

    headers = {
        'Authorization': f'Bearer {gcp_access_token}',
        'Content-Type': 'application/json'
    }

    # URL for Google Cloud Storage Transfer API
    base_url = f'https://storagetransfer.googleapis.com/v1/{job_name if job_name else "transferJobs"}'

    # Data for creating or updating the transfer job
    transfer_job_data = {
        'projectId': project_id,
        'transferSpec': {
            'gcsDataSource': {
                'bucketName': aws_s3bucket_name
            },
            'gcsDataSink': {
                'bucketName': gcp_bucket_name
            },
            'objectConditions': {
                'includePrefixes': filenames  # Use the list of filenames from the event
            },
            'transferOptions': {
                'deleteObjectsFromSourceAfterTransfer': delete_after_transfer
            }
        },
        'schedule': {
            'scheduleStartDate': {
                'year': datetime.datetime.now().year,
                'month': datetime.datetime.now().month,
                'day': datetime.datetime.now().day
            },
            'startTimeOfDay': {
                'hours': 12,
                'minutes': 0,
                'seconds': 0
            }
        },
        'status': 'ENABLED'
    }
    logger.info(f'GCP API request url: {base_url}')
    logger.info(f'Transfer job: {json.dumps(transfer_job_data)}')
    # Execute the HTTP request to create or update the job
    try:
        if job_name:
            response = requests.patch(base_url, headers=headers, data=json.dumps(transfer_job_data))
        else:
            response = requests.post(base_url, headers=headers, data=json.dumps(transfer_job_data))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except requests.exceptions.RequestException as defined_error:
        logger.info(f"Failed to make API request: {defined_error}")
        return {
            'statusCode': 500,
            'body': {'error': str(defined_error)}
        }