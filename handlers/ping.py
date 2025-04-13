from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/db")
async def ping_db():
    return {"message": "ok"}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}




