from fastapi import APIRouter

router = APIRouter()

@router.get("/api/", tags=["api"])
async def testAPI():
  return {"testando rota API"}