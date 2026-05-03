"""
Apps module routes: create, list, get-by-id.
"""

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from pydantic import BaseModel
from app.db.mongo import db
from app.models.app_model import AppCreate, AppOut
from app.deps.auth import get_current_user

router = APIRouter(prefix="/apps", tags=["apps"])


def serialize(doc) -> dict:
    """Convert Mongo document to JSON-serializable dict."""
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc.get("description"),
        "url": doc["url"],
        "category": doc.get("category"),
    }


@router.post("/", response_model=AppOut)
async def create_app(app: AppCreate, current=Depends(get_current_user)):
    """Create a new app (protected)."""
    doc = app.dict()
    doc["owner_id"] = current["user_id"]

    res = await db.apps.insert_one(doc)
    created = await db.apps.find_one({"_id": res.inserted_id})
    return serialize(created)


@router.get("/", response_model=list[AppOut])
async def list_apps():
    """List all apps (public)."""
    cursor = db.apps.find().sort("_id", -1)
    items = []
    async for doc in cursor:
        items.append(serialize(doc))
    return items


@router.get("/{app_id}", response_model=AppOut)
async def get_app(app_id: str):
    """Get app by id."""
    if not ObjectId.is_valid(app_id):
        raise HTTPException(status_code=400, detail="Invalid id")

    doc = await db.apps.find_one({"_id": ObjectId(app_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="App not found")

    return serialize(doc)





class AppIdRequest(BaseModel):
    id: str


@router.post("/get")
async def get_app_by_body(req: AppIdRequest):
    doc = await db.apps.find_one({"_id": ObjectId(req.id)})

    if not doc:
        raise HTTPException(status_code=404, detail="App not found")

    return serialize(doc)