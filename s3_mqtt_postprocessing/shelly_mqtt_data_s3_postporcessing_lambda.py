import logging
import json
import boto3
from datetime import datetime, timedelta, timezone

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    has_more_files = False
    logger.info("Start of the function")
    # Calculate the date to process (yesterday)
    process_date = datetime.now(timezone.utc) - timedelta(days=1)
    date_prefix = process_date.strftime('%Y/%m/%d')
    bucket_name = 'mozharovskyi-shelly-gcp-raw-mqtt-storage-eu-central-1'
    main_directories = ['MozharovskysEM']
    transfer_files = list()

    # Process each directory
    for main_dir in main_directories:
        prefix = f'{main_dir}/{date_prefix}/'
        logger.info(f"Processing directory: {prefix}")
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix,
                                           PaginationConfig={'MaxItems': 50, 'PageSize': 50})
        # Iterate through pages of results
        for page in page_iterator:
            combined_data = []
            files_to_delete = []
            if 'Contents' in page:
                for item in page['Contents']:
                    file_key = item['Key']
                    # Skip the aggregated file based on its name pattern
                    if file_key.endswith(f'{process_date.strftime("%Y-%m-%d")}.json'):
                        logger.info(f"Skipping aggregated file: {file_key}")
                        continue
                    # Read and process the file
                    file_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                    file_content = file_response['Body'].read().decode('utf-8')
                    json_content = json.loads(file_content)
                    json_content.pop('id', None)
                    json_content.pop('calibration', None)
                    json_content['timestamp'] = file_key.split('/')[-1].split('.')[0]
                    combined_data.append(json_content)
                    files_to_delete.append({'Key': file_key})
            combined_filename = f'{process_date.strftime("%Y-%m-%d")}.json'
            combined_filepath = f'{prefix}{combined_filename}'
            # Check if the aggregated file already exists
            try:
                existing_data = s3_client.get_object(Bucket=bucket_name, Key=combined_filepath)
                existing_content = json.loads(existing_data['Body'].read().decode('utf-8'))
                combined_data.extend(existing_content)
                logger.info(f"Existing aggregated data found and merged: {combined_filepath}")
            except s3_client.exceptions.NoSuchKey:
                logger.info("No existing file, creating new one")
            # Write aggregated data
            s3_client.put_object(Bucket=bucket_name, Key=combined_filepath, Body=json.dumps(combined_data))
            if files_to_delete:
                delete_response = s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': files_to_delete}
                )
                logger.info(f"Deleted processed files: {len(files_to_delete)} files")
            logger.info(f"Batch for {main_dir} processed and files deleted")
    # Re-check each directory for remaining files
    for main_dir in main_directories:
        prefix = f'{main_dir}/{date_prefix}/'
        logger.info(f"Re-checking directory for remaining files: {prefix}")
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix,
                                           PaginationConfig={'MaxItems': 50, 'PageSize': 50})
        # Iterate through pages of results
        for page in page_iterator:
            if 'Contents' not in page:
                continue
            for item in page['Contents']:
                file_key = item['Key']
                # Skip the aggregated file
                if not file_key.endswith(f'{process_date.strftime("%Y-%m-%d")}.json'):
                    # If another file is found, set the flag to True and exit early
                    has_more_files = True
                    break
            if has_more_files:
                break
    # Return the result
    logger.info(f"Are there more files to process? {has_more_files}")
    if not has_more_files:
        for main_dir in main_directories:
            prefix = f'{main_dir}/{date_prefix}/'
            combined_filename = f'{process_date.strftime("%Y-%m-%d")}.json'
            combined_filepath = f'{prefix}{combined_filename}'
            transfer_files.append(combined_filepath)
    logger.info("End of the function")
    message = "All data processed for all directories" if not has_more_files else "There are more data to process"
    return {
        'hasMoreFiles': has_more_files,
        'filenames': transfer_files,
        'body': json.dumps(message)
    }