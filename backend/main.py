from contextlib import asynccontextmanager

import strawberry

from fastapi import FastAPI, Depends, Request, WebSocket, BackgroundTasks
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from db import engine
from models import User, Service, Incident
from sqlmodel import Session, SQLModel
from schema import schema

def createDBtables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    createDBtables()
    yield 

def get_session():
    with Session(engine) as session:
        yield session

async def get_context(session: Session = Depends(get_session)):
    return {
        "session": session,
    }

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context 
)

app.include_router(graphql_app, prefix="/graphql")

#ruta de baza
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}