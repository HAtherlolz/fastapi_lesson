from fastapi import APIRouter

from api.endpoints.v1.profiles import api_profiles

api_router = APIRouter()

api_router.include_router(api_profiles, prefix='/api/v1', tags=["profile"])
