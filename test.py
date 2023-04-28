from aiohttp import ClientSession


async def ip_check(ip) -> None:
    """
        Converting the latitude and longitude
        to city, region and country
    """
    url = f'http://ip-api.com/json/{ip}'
    async with ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            location = await response.json()
            print(location)


await ip_check()