from contextlib import asynccontextmanager
from datetime import datetime
from time import mktime
from typing import List
from collections import defaultdict
from abc import ABC, abstractmethod

import asyncio
import feedparser
import strawberry
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI, Depends, Request, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlmodel import Session, SQLModel, select, delete, desc

from emails import trimite_email_breaking_news
from db import engine
from models import NewsSource, Article, Subscriber
from schema import schema, ArticleModel

import re
import html

origins = [
    "http://localhost:5173"
]

def curata_html(text_brut: str) -> str:
    if not text_brut:
        return "Nicio descriere."

    text_decodat = html.unescape(text_brut)

    text_curat = re.sub(r'<[^>]+>', '', text_decodat)
    
    return text_curat.strip()


async def monitor_stiri():

    await asyncio.sleep(5) 
    
    while True:
        try:
            with Session(engine) as session:

                surse = session.exec(select(NewsSource)).all()
                
                if not surse:
                    print(" Nu ai adăugat nicio sursa de stiri in baza de date.")
                
                for sursa in surse:
            
                    statement = select(Article).where(Article.source_id == sursa.id).order_by(desc(Article.date)).limit(1)
                    ultimul_articol = session.exec(statement).first()
                    
                    ultima_data_db = ultimul_articol.date if ultimul_articol else datetime(2026, 7, 7)
                    
                    feed = feedparser.parse(sursa.url)
                    stiri_noi_gasite = 0
                    
                    for entry in feed.entries[::-1]:
                        # Ne asigurăm că știrea are o dată validă în ea
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            data_articol = datetime.fromtimestamp(mktime(entry.published_parsed))

                            if data_articol > ultima_data_db:
                                print(f"   BREAKING NEWS gasit: {entry.title}")
                                
                                nou_articol = Article(
                                    title=entry.title,
                                    description=curata_html(entry.get("summary", "")),
                                    link=entry.get("link", ""),
                                    date=data_articol,
                                    source_id=sursa.id
                                )
                                
                                session.add(nou_articol)
                                stiri_noi_gasite += 1
                                abonati = session.exec(select(Subscriber).where(Subscriber.is_active == True)).all()
                                lista_emailuri = [abonat.email for abonat in abonati]
    
                                trimite_email_breaking_news(
                                    emailuri_destinatari=lista_emailuri,
                                    sursa_nume=sursa.name,
                                    titlu_stire=entry.title,
                                    link_stire=entry.link
                                )
                    
                    if stiri_noi_gasite > 0:
                        session.commit()
                        print(f" ALARMA: S-au salvat si trimis catre utilizatori {stiri_noi_gasite} stiri noi de la {sursa.name}!")
                    else:
                        print(f"  Nimic nou la {sursa.name}.")
                        
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f" Eroare critica în bucla: {e}")
            
        finally:
            print("Final scanare. Ne vedem peste 30 de minute.\n")
            await asyncio.sleep(60)

def createDBtables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    createDBtables()
    monitor_task = asyncio.create_task(monitor_stiri())
    
    yield 
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        print("Bucla de monitorizare a fost oprita ok.")

def get_session():
    with Session(engine) as session:
        yield session

#the dataloader part

async def get_context(session: Session = Depends(get_session)):
    async def load_articles_by_service(keys: List[int]) -> List[List[ArticleModel]]:
        statement = select(ArticleModel).where(ArticleModel.source_id.in_(keys))
        Articles = session.exec(statement).all()
        Articles_group = defaultdict(list)
        for Article in Articles:
            Articles_group[Article.source_id].append(Article)
            
        return [Articles_group[key] for key in keys]


    return {
        "session": session,
        "Articles_loader": DataLoader(load_fn=load_articles_by_service)
    }

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}


app.include_router(graphql_app, prefix="/graphql")