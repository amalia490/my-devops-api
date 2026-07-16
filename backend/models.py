from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class NewsSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)         
    url: str                                
    category: Optional[str] = Field(default="General") 

    articles: List["Article"] = Relationship(back_populates="source")

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str                             
    description: str                      
    link: str                              
    date: datetime = Field(index=True)      
    source_id: int = Field(default=None, foreign_key="newssource.id")
    source: Optional[NewsSource] = Relationship(back_populates="articles")

class Subscriber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)