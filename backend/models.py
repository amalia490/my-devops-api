from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique = True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    status: str = Field(index=True)
    incidents: List["Incident"] = Relationship(back_populates="service")
    
class Incident(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_id: int | None = Field(default=None, foreign_key = "service.id")
    description: str
    resolved: bool
    service: Optional[Service] = Relationship(back_populates="incidents")

