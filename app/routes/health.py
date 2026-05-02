from fastapi import APIRouter
from app.db.mongo import db

router = APIRouter()

@router.get("/")
async def root():
    await db.test.insert_one({"status": "working"})
    return {"message": "MongoDB connected 🚀"}