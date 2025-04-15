import asyncio
from crawlers import crawler_livelo_partners

async def main():
    result = await crawler_livelo_partners.get_livelo_partners()
    with open('data/response.json', 'w', encoding='utf-8') as f:
        f.write(result.text)
    # print(result.text)

if __name__ == "__main__":
    asyncio.run(main())