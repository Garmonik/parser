from fastapi import APIRouter

from .endpoints.parser import router as parser_routers

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(parser_routers, prefix="/parser", tags=["Parser"])
