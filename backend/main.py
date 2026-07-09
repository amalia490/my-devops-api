from contextlib import asynccontextmanager
import strawberry
from strawberry.dataloader import DataLoader
from fastapi import FastAPI, Depends, Request, WebSocket, BackgroundTasks
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from db import engine
from models import User, Service, Incident
from sqlmodel import Session, SQLModel
from schema import schema
from sqlmodel import select
from schema import IncidentModel
from typing import List 
from collections import defaultdict 
def createDBtables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    createDBtables()
    yield 

def get_session():
    with Session(engine) as session:
        yield session

#the dataloader part

async def get_context(session: Session = Depends(get_session)):
    async def load_incidents_by_service(keys: List[int]) -> List[List[IncidentModel]]:
        statement = select(IncidentModel).where(IncidentModel.service_id.in_(keys))
        incidents = session.exec(statement).all()
        incidents_group = defaultdict(list)
        for incident in incidents:
            incidents_group[incident.service_id].append(incident)
            
        return [incidents_group[key] for key in keys]


    return {
        "session": session,
        "incidents_loader": DataLoader(load_fn=load_incidents_by_service)
    }

app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context 
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}


app.include_router(graphql_app, prefix="/graphql")