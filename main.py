from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqladmin import Admin

from config.conf import settings
from config.database import engine, create_tables

from api.endpoints.api_router import api_router
from api.endpoints.admin.admin_views import ProfileAdmin

app = FastAPI(
    openapi_url="/api/v1/",
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/",

    title="IVAN'S PYTHON",
    description="API's for Ivan's lesson",
    version="0.1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await create_tables()


app.include_router(api_router)

# Admin panel
admin = Admin(app, engine, "/api/v1/admin/")
admin.add_view(ProfileAdmin)
