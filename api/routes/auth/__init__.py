from fastapi import APIRouter
from .auth import router as auth_router
from .discord_oauth import router as discord_oauth_router

# Create main auth router and include sub-routers
router = APIRouter()
router.include_router(auth_router)
router.include_router(discord_oauth_router)

__all__ = ["router"]
