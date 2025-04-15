import httpx
from loguru import logger
# import sys
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def get_livelo_partners() -> httpx.Response:
    logger.info("Starting to fetch Livelo Partners page")
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

    logger.info(f"Finished to fetch Livelo Partners page. Status code: {response.status_code}")
    return response


if __name__ == "__main__":
    try:
        response = asyncio.run(get_livelo_partners())
        logger.info(f"Finished to fetch data successfully. Status code: {response.status_code}")
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to fetch data: {e.response.status_code} - {e.response.text}")
        raise e
