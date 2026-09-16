from contextlib import asynccontextmanager
from datetime import datetime
from time import mktime
from typing import List
from collections import defaultdict
from abc import ABC, abstractmethod
import json
import asyncio
import unicodedata
import feedparser
import strawberry
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI, Depends, Request, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlmodel import Session, SQLModel, select, delete, desc, func

from emails import trimite_email_breaking_news
from db import engine
from models import NewsSource, Article, Subscriber, CountyArticle, County
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
                toate_judetele = session.exec(select(County)).all()
                
                if not surse:
                    print("Nu ai adăugat nicio sursa de stiri in baza de date.")
                
                
                judete_procesate = []
                for j in toate_judetele:
                
                    lista_cuvinte = [cuvant.strip().lower() for cuvant in j.key_words.split(',')]
                    if j.name.lower() not in lista_cuvinte:
                        lista_cuvinte.append(j.name.lower())
                
                    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, lista_cuvinte)) + r')\b')
                    judete_procesate.append((j, pattern))

                for sursa in surse:
                    statement = select(Article).where(Article.source_id == sursa.id).order_by(desc(Article.date)).limit(1)
                    ultimul_articol = session.exec(statement).first()
                    ultima_data_db = ultimul_articol.date if ultimul_articol else datetime(2026, 7, 7)
                
                    feed = await asyncio.to_thread(feedparser.parse, sursa.url)
                    
                    stiri_noi_salvate = [] 
                                                                        
                    for entry in feed.entries[::-1]:
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            data_articol = datetime.fromtimestamp(mktime(entry.published_parsed))

                            if data_articol > ultima_data_db:
                                print(f"  BREAKING NEWS gasit: {entry.title}")
                                
                                lat = entry.get('geo_lat') or None
                                lng = entry.get('geo_long') or None
                                            
                                nou_articol = Article(
                                    title=entry.title,
                                    description=curata_html(entry.get("summary", "")),
                                    link=entry.get("link", ""),
                                    date=data_articol,
                                    source_id=sursa.id,
                                    latitude=lat,
                                    longitude=lng
                                )
                                
                                titlu = entry.get('title', 'Fără titlu')
                                summary = entry.get('summary', '')
                                description = entry.get('description', '')
                                text_complet = f"{titlu} {summary} {description}".lower()
                    
                                for j, pattern in judete_procesate:
                                    if pattern.search(text_complet):
                                        nou_articol.counties.append(j)

                                session.add(nou_articol)
                                stiri_noi_salvate.append(nou_articol)

                    if stiri_noi_salvate:
                        session.commit()
                        
                        abonati = session.exec(select(Subscriber).where(Subscriber.is_active == True)).all()
                        lista_emailuri = [abonat.email for abonat in abonati]

                        for articol in stiri_noi_salvate:
                            await asyncio.to_thread(
                                trimite_email_breaking_news,
                                emailuri_destinatari=lista_emailuri,
                                sursa_nume=sursa.name,
                                titlu_stire=articol.title,
                                link_stire=articol.link
                            )
                            
                        print(f" ALARMA: S-au salvat si trimis catre utilizatori {len(stiri_noi_salvate)} stiri noi de la {sursa.name}!")
                    else:
                        print(f"  Nimic nou la {sursa.name}.")
                        
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f" Eroare critica în bucla: {e}")
            
        finally:
            print("Final scanare. Ne vedem peste 30 de minute.\n")
            await asyncio.sleep(1800)
            
def remove_diacritics(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

def generate_keywords(county_name: str) -> str:
    name_lower = county_name.lower()
    name_no_diacritics = remove_diacritics(name_lower)
    keywords = {name_lower, name_no_diacritics, f"judetul {name_no_diacritics}"}
    
    if "bucure" in name_lower:
        political_words = [
            "capitala", "parlament", "parlamentul", "partid", "partide", 
            "psd", "pnl", "usr", "aur", "udmr", "sos", 
            "guvern", "guvernul", "sistem", "politica", "politic", 
            "minister", "senat", "deputati", "alegeri"
        ]
        keywords.update(political_words)
    return ", ".join(keywords)

def createDBtables():
    
    file_path = "romania-counties.json"
    with open(file_path, "r", encoding="utf-8") as fisier:
        date_judete = json.load(fisier)
        
    with Session(engine) as session:
        geometries = date_judete.get("objects", {}).get("ROU_adm1", {}).get("geometries", [])
        
        for geo in geometries:
            nume_judet = geo.get("properties", {}).get("NAME_1")
            
            if not nume_judet:
                continue
            existing_county = session.exec(
                select(County).where(County.name == nume_judet)
            ).first()
            
            if not existing_county:
                judet_keywords = generate_keywords(nume_judet)
                
                judet = County(
                    name=nume_judet,
                    key_words= judet_keywords
                )
                session.add(judet)
        session.commit()
        print("Baza de date a fost populată cu județele din JSON!")
        
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

    async def load_count_by_county(keys: List[int]) -> List[int]:
        statement = (
            select(
                CountyArticle.county_id,
                func.count(CountyArticle.article_id)
            )
            .where(CountyArticle.county_id.in_(keys))
            .group_by(CountyArticle.county_id)
        )
        CountyArticles = session.exec(statement).all()
        counts_map = {county_id: count for county_id, count in CountyArticles}
        
        return [counts_map.get(county_id, 0) for county_id in keys]
    
    return {
        "session": session,
        "Articles_loader": DataLoader(load_fn=load_articles_by_service),
        "Counties_loader": DataLoader(load_fn=load_count_by_county)
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