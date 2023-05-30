import aiohttp
import asyncio
from candore.modules.api_lister import api_endpoints
from candore.config import settings


async def fetch_entities(url):
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(settings.candore.username, settings.candore.password), connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error: {response.status}")
                return None


async def process_entities(url):
    data = await fetch_entities(url)
    if data:
        return data.get('results', None)


async def extract_entities():
    all_data = {}
    for component, endpoints in api_endpoints.lister_endpoints().items():
        if endpoints:
            comp_entities = await process_entities(url=settings.candore.base_url + endpoints[0])
            all_data[component] = comp_entities
    return all_data


async def print_entities():
    import json
    data = await extract_entities()
    with open('preentities.json', 'w') as entfile:
        json.dump(data, entfile)

