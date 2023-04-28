from aiohttp import ClientSession

from fastapi import HTTPException, status

from config.conf import settings


async def convert_coords_to_locs(lat: float, lng: float) -> tuple[str, str]:
    """
        Converting the latitude and longitude
        to city, region and country
    """
    url = f'{settings.LEAFLET}?lat={lat}&lon={lng}&accept-language=ua&format=json'
    async with ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            location = await response.json()
            try:
                country = location['address']['country']
                # GET City, if no city, GET village
                try:
                    city = location['address']['city']
                except KeyError:
                    # GET village, if no village, GET municipality
                    try:
                        city = location['address']['village']
                    except KeyError:
                        city = location['address']['municipality']
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The coordinates is not valid."
                )
    return country, city
