from fastapi import FastAPI
from .routes import api

app = FastAPI()
app.include_router(api.router)


@app.get("/")
async def root():
  return {"message": "Testando"}