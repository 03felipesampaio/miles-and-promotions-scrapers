import httpx
from loguru import logger
# import sys
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from google.cloud import storage
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def get_livelo_partners() -> httpx.Response:
    logger.info("Trying to fetch Livelo Partners page")
    url = (
        "https://apis.pontoslivelo.com.br/api-bff-partners-parities/v1/parities/active"
    )
    client = httpx.AsyncClient(timeout=2.0)
    response = await client.get(url)

    try:
        response.raise_for_status()  # Raise an error for bad responses
    except httpx.HTTPStatusError as e:
        logger.error(f"Error fetching data: {e.response.status_code} - {e.response.text}")
        raise e

    logger.info(f"Successfuly fetched Livelo Partners page. Status code: {response.status_code}")
    return response


def write_to_gcp_bucket(bucket_name: str, destination_blob_name: str, data: str):
    """
    Writes data to a GCP bucket.

    :param bucket_name: Name of the GCP bucket.
    :param destination_blob_name: The name of the file to be created in the bucket.
    :param data: The data to write to the bucket.
    """
    logger.info(f"Uploading data to GCP bucket: {bucket_name}, file: {destination_blob_name}")
    try:
        # Initialize the GCP storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the data
        blob.upload_from_string(data)
        logger.info(f"Data successfully uploaded to {bucket_name}/{destination_blob_name}")
    except Exception as e:
        logger.error(f"Failed to upload data to GCP bucket: {e}")
        raise e


if __name__ == "__main__":
    logger.info("Starting to fetch Livelo Partners page")
    response = asyncio.run(get_livelo_partners())
    logger.info(f"Finished to fetch data successfully. Status code: {response.status_code}")
    if response.status_code == 200:
        # Write the response content to a GCP bucket
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        today = datetime.now(timezone.utc)
        destination_blob_name = f"livelo/{today.year}/{today.month}/{today.strftime('%Y%m%d')}_livelo_partners_api_response.json"
        write_to_gcp_bucket(bucket_name, destination_blob_name, response.text)
