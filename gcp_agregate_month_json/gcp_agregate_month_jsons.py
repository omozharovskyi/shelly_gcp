import logging
from google.cloud import storage
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

# Setuping logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def aggregate_jsonl_files(*args, **kwargs):
    # Logging called parameters
    logger.info(f"Called aggregate_jsonl_files with args: {args}, kwargs: {kwargs}")
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    bucket_name = 'mozharovskyi-shelly-gcp-agregated-mqtt-storage-eu'
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception as get_bucket_faulure:
        logger.error(f"Failed to get bucket: {get_bucket_faulure}")
        return f"Failed to get bucket: {get_bucket_faulure}\n", 500
    # Determine the year and month for processing files. Get the current date in UTC
    today = datetime.now(timezone.utc)
    previous_month_date = today - relativedelta(months=1)
    year = previous_month_date.strftime('%Y')
    month = previous_month_date.strftime('%m')
    prefix = f'{year}/{month}/'
    # Collect files to process
    try:
        blobs = bucket.list_blobs(prefix=prefix)
    except Exception as blob_list_exception:
        logger.error(f"Failed to list blobs: {blob_list_exception}")
        return f"Failed to list blobs: {blob_list_exception}\n", 500
    logger.info(f'Found files: {blobs}')
    user_data = {}
    for blob in blobs:
        user = blob.name.split('/')[0]
        logger.info(f'Found user in blob name: {user}')
        if user not in user_data:
            user_data[user] = []
        try:
            content = blob.download_as_text()
            user_data[user].extend(content.strip().split('\n'))
        except Exception as reading_blob_exception:
            logger.error(f"Error downloading blob {blob.name}: {reading_blob_exception}")
            return f"Error downloading blob {blob.name}: {reading_blob_exception}\n", 500
    # Write aggregated files
    for user, data in user_data.items():
        aggregated_filename = f'{user}/{year}/{year}-{month}.json'
        logger.info(f'Agregated blob name: {aggregated_filename}')
        aggregated_blob = bucket.blob(aggregated_filename)
        try:
            aggregated_blob.upload_from_string('\n'.join(data))
            # Delete processed files
            # for blob in bucket.list_blobs(prefix=f'{user}/{prefix}'):
            #     blob.delete()
        except Exception as writing_agregated_exception:
            logger.error(f"Error processing data for user {user}: {writing_agregated_exception}")
            return f"Error processing data for user {user}: {writing_agregated_exception}\n", 500
    logger.info("Data aggregation and processing completed successfully.")
    return "Data aggregation and processing completed successfully.\n", 200
