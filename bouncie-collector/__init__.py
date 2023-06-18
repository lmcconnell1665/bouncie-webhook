import logging
import boto3
import json
import os
from datetime import datetime
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Read the JSON data from the request body
        json_data = req.get_json()
        event_type = json_data['eventType']
        current_timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        logging.info(f'Event type: {event_type}')
        logging.info(f'Current timestamp: {current_timestamp}')
        logging.debug(f'JSON data: {json_data}')

        # Save the JSON data to a temporary file
        temp_file_path = '/tmp/temp.json'  # Use an appropriate temporary file path
        with open(temp_file_path, 'w') as file:
            json.dump(json_data, file)

        # Upload the temporary file to S3
        s3_bucket_name = 'mcconnell.privatefiles'
        s3_folder_name = 'BouncieGPSData'
        s3_key = f'{s3_folder_name}/{event_type}_{current_timestamp}.json'  # Specify the desired S3 file path and name
        s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'))
        s3_client.upload_file(temp_file_path, s3_bucket_name, s3_key)

        logging.info(f'JSON data saved to S3: {s3_key}')

        # Delete the temporary file
        os.remove(temp_file_path)

        # Return a success response
        return func.HttpResponse(status_code=200)
    except Exception as e:
        # Handle any exceptions and return an error response
        logging.error(str(e))
        return func.HttpResponse(status_code=500)
