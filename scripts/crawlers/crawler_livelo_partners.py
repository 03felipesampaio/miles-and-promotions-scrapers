import httpx
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def get_livelo_partners() -> httpx.Response:
    url = (
        "https://apis.pontoslivelo.com.br/api-bff-partners-parities/v1/parities/active"
    )
    client = httpx.AsyncClient(timeout=2.0)
    response = await client.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response


if __name__ == "__main__":
    response = asyncio.run(get_livelo_partners())
