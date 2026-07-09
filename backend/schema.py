from collections import defaultdict
import typing
import strawberry
from strawberry.types import Info
from sqlmodel import select
from typing import Optional
from models import User as UserModel, Service as ServiceModel, Incident as IncidentModel
from typing import List
from strawberry.dataloader import DataLoader

@strawberry.type
class User:
    id: int
    email: str
    created_at: str
    
@strawberry.type
class Incident:
    id: int
    service_id: int
    description: str
    resolved: bool
    
@strawberry.type
class Service:
    id: int
    name: str
    status: str
    
    @strawberry.field
    #resolver pentru campul 'incidents'
    async def incidents(self, info: Info) -> List[Incident]:
        return await info.context["incidents_loader"].load(self.id)
    
@strawberry.input
class ServiceUpdateInput:
    name: Optional[str] = None
    status: Optional[str] = None
    
@strawberry.input
class UserUpdateInput:
    email: Optional[str] = None
    created_at: Optional[str] = None

@strawberry.input
class IncidentUpdateInput:
    service_id: Optional[int] = None
    description: Optional[str] = None
    resolved: Optional[bool] = None 
    
def get_users(info: Info):
    session = info.context["session"]
    return session.exec(select(UserModel)).all()

def get_user_id(info: Info, user_id: int):
    session = info.context["session"]
    return session.get(UserModel, user_id)

def get_service(info: Info):
    session = info.context["session"]
    return session.exec(select(ServiceModel)).all()
     
def get_services_id(info: Info, service_ids: List[int]) -> List[Service]:
    session = info.context["session"]
    statement = select(ServiceModel).where(ServiceModel.id.in_(service_ids))
    return session.exec(statement).all()

def get_incidents(info: Info):
    session = info.context["session"]
    return session.exec(select(IncidentModel)).all()
    
def get_incident_id(info: Info, incident_id: int):
    session = info.context["session"]
    return session.get(IncidentModel, incident_id)

@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=get_users)
    user_by_id: User = strawberry.field(resolver=get_user_id)
    services: typing.List[Service]= strawberry.field(resolver=get_service)
    services_by_id: List[Service] = strawberry.field(resolver=get_services_id)
    incidents: typing.List[Incident]= strawberry.field(resolver=get_incidents)
    incident_by_id: Incident = strawberry.field(resolver=get_incident_id)    

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, info:Info, email:str, created_at:str) -> User:
        session = info.context["session"]
        new_user = UserModel(email=email, created_at = created_at)
        session.add(new_user)
        session.commit()
        
        session.refresh(new_user)
        
        return new_user
    
    @strawberry.mutation
    def add_service(self, info: Info, name:str, status:str) -> Service:
        session = info.context["session"]
        new_service = ServiceModel(name=name, status=status)
        session.add(new_service)
        session.commit()
        
        session.refresh(new_service)
        
        return new_service
    
    @strawberry.mutation
    def add_incident(self, info:Info, service_id:int, description:str, resolved:bool) -> Incident:
        session = info.context["session"]
        new_incident = IncidentModel(service_id = service_id, description = description, resolved = resolved)
        session.add(new_incident)
        session.commit()
        
        session.refresh(new_incident)
        
        return new_incident 
    
    @strawberry.mutation
    def update_service(self, info: Info, service_id: int, data: ServiceUpdateInput) -> Service:
        session = info.context["session"]
        service = session.get(ServiceModel, service_id)
        if not service:
            raise Exception(f"Serviciul cu ID {service_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(service, key, value)
                
        session.add(service)
        session.commit()
        session.refresh(service)
        
        return service
    
    @strawberry.mutation
    def update_user(self, info: Info, user_id: int, data:UserUpdateInput) -> User:
        session = info.context["session"]
        user = session.get(UserModel, user_id)
        
        if not user:
            raise Exception(f"Userul cu ID {user_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
                
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user
        
    @strawberry.mutation
    def update_incident(self, info:Info, incident_id: int, data: IncidentUpdateInput) -> Incident:
        session = info.context["session"]
        incident = session.get(IncidentModel, incident_id)
        
        if not incident:
            raise Exception(f"Incidentul cu ID {incident_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(incident, key, value)
                
        session.add(incident)
        session.commit()
        session.refresh(incident)
        
        return incident
        
    @strawberry.mutation
    def delete_service(self, info:Info, service_id: int) -> bool:
        session = info.context["session"]
        
        service = session.get(ServiceModel, service_id)
        if not service:
            return False

        session.delete(service)

        session.commit()
        return True
    
    @strawberry.mutation
    def delete_user(self, info:Info, user_id: int) -> bool:
        session = info.context["session"]
        
        user = session.get(UserModel, user_id)
        if not user:
            return False

        session.delete(user)

        session.commit()
        return True
    
    @strawberry.mutation
    def delete_incident(self, info:Info, incident_id: int) -> bool:
        session = info.context["session"]
        
        incident = session.get(IncidentModel, incident_id)
        if not incident:
            return False

        session.delete(incident)

        session.commit()
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
