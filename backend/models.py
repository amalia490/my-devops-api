from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class NewsSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)         
    url: str                                
    category: Optional[str] = Field(default="General") 

    articles: List["Article"] = Relationship(back_populates="source")

class CountyArticle(SQLModel, table=True):
    article_id: int | None = Field(default=None, foreign_key="article.id", primary_key=True)
    county_id: int | None = Field(default=None, foreign_key="county.id", primary_key=True)
    
    
class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str                             
    description: str                      
    link: str                              
    date: datetime = Field(index=True)      
    source_id: int = Field(default=None, foreign_key="newssource.id")
    source: Optional[NewsSource] = Relationship(back_populates="articles")
    counties: List["County"] = Relationship(back_populates="articles", link_model=CountyArticle)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Subscriber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    
class County(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    key_words: str 
    latitude: Optional[float] = Field(default=0.0) 
    longitude: Optional[float] = Field(default=0.0)
    articles: List["Article"] = Relationship(back_populates="counties", link_model=CountyArticle)



    