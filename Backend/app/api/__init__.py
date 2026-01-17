from app.api.endpoints import router as api_router
from app.api.ws_endpoints import router as ws_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(api_router)
router.include_router(ws_router)