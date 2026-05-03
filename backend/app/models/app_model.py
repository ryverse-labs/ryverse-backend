"""
Pydantic models for Apps module.
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional


class AppCreate(BaseModel):
    name: str
    description: Optional[str] = None
    url: HttpUrl
    category: Optional[str] = "general"


class AppOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    url: HttpUrl
    category: Optional[str]