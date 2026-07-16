from collections import defaultdict
import typing
import strawberry
from strawberry.types import Info
from sqlmodel import select
from typing import Optional
from models import Subscriber as SubscriberModel, NewsSource as NewsSourceModel, Article as ArticleModel
from typing import List
from strawberry.dataloader import DataLoader

@strawberry.type
class Subscriber:
    id: int
    email: str
    is_active: bool
    
@strawberry.type
class Article:
    id: int
    title: str
    link: str
    source_id: int
    description: str
    date: str 
    
@strawberry.type
class NewsSource:
    id: int
    name: str
    url: str
    category: str
    
    @strawberry.field
    #resolver pentru campul 'Articles'
    async def Articles(self, info: Info) -> List[Article]:
        return await info.context["Articles_loader"].load(self.id)
    
@strawberry.input
class NewsSourceUpdateInput:
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    
@strawberry.input
class SubscriberUpdateInput:
    email: Optional[str] = None
    is_active: Optional[bool] = None

@strawberry.input
class ArticleUpdateInput:
    title: Optional[str] = None
    link: Optional[str] = None
    date: Optional[str] = None
    NewsSource_id: Optional[int] = None
    description: Optional[str] = None
    
def get_Subscribers(info: Info):
    session = info.context["session"]
    return session.exec(select(SubscriberModel)).all()

def get_Subscriber_id(info: Info, Subscriber_id: int):
    session = info.context["session"]
    return session.get(SubscriberModel, Subscriber_id)

def get_NewsSource(info: Info):
    session = info.context["session"]
    return session.exec(select(NewsSourceModel)).all()
     
def get_NewsSources_id(info: Info, NewsSource_id: int) -> NewsSource:
    session = info.context["session"]
    return session.get(NewsSourceModel, NewsSource_id)

def get_Articles(info: Info):
    session = info.context["session"]
    return session.exec(select(ArticleModel)).all()
    
def get_Article_id(info: Info, Article_id: int):
    session = info.context["session"]
    return session.get(ArticleModel, Article_id)

@strawberry.type
class Query:
    Subscribers: typing.List[Subscriber] = strawberry.field(resolver=get_Subscribers)
    Subscriber_by_id: Subscriber = strawberry.field(resolver=get_Subscriber_id)
    NewsSources: typing.List[NewsSource]= strawberry.field(resolver=get_NewsSource)
    NewsSources_by_id: NewsSource = strawberry.field(resolver=get_NewsSources_id)
    Articles: typing.List[Article]= strawberry.field(resolver=get_Articles)
    Article_by_id: Article = strawberry.field(resolver=get_Article_id)    

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_Subscriber(self, info:Info, email:str, is_active:bool) -> str:
        session = info.context["session"]
        sbc_exista = session.exec(
                select(SubscriberModel).where(SubscriberModel.email == email)
            ).first()
            
        if sbc_exista:
            if not sbc_exista.is_active:
                sbc_exista.is_active = True
                session.add(sbc_exista)
                session.commit()
                return "Te-ai reabonat cu succes la alerte!"
            return "Esti deja abonat la alertele noastre!"
            
        new_Subscriber = SubscriberModel(email=email, is_active = is_active)
        session.add(new_Subscriber)
        session.commit()
        
        session.refresh(new_Subscriber)
        
        return "Te-ai abonat cu succes la alerte!"
    
    @strawberry.mutation
    def add_NewsSource(self, info: Info, name:str, url:str, category:str) -> NewsSource:
        session = info.context["session"]
        new_NewsSource = NewsSourceModel(name=name, url=url, category= category)
        session.add(new_NewsSource)
        session.commit()
        
        session.refresh(new_NewsSource)
        
        return new_NewsSource
    
    @strawberry.mutation
    def add_Article(self, info:Info, NewsSource_id:int, description:str, title:str, link:str, date:str) -> Article:
        session = info.context["session"]
        new_Article = ArticleModel(NewsSource_id = NewsSource_id, description = description, title = title, link = link, date = date)
        session.add(new_Article)
        session.commit()
        
        #trimite_email_abonati(new_Article.title)
        
        session.refresh(new_Article)
        
        return new_Article 
    
    @strawberry.mutation
    def update_NewsSource(self, info: Info, NewsSource_id: int, data: NewsSourceUpdateInput) -> NewsSource:
        session = info.context["session"]
        NewsSource = session.get(NewsSourceModel, NewsSource_id)
        if not NewsSource:
            raise Exception(f"Serviciul cu ID {NewsSource_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(NewsSource, key, value)
                
        session.add(NewsSource)
        session.commit()
        session.refresh(NewsSource)
        
        return NewsSource
    
    @strawberry.mutation
    def update_Subscriber(self, info: Info, Subscriber_id: int, data:SubscriberUpdateInput) -> Subscriber:
        session = info.context["session"]
        Subscriber = session.get(SubscriberModel, Subscriber_id)
        
        if not Subscriber:
            raise Exception(f"Subscriberul cu ID {Subscriber_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(Subscriber, key, value)
                
        session.add(Subscriber)
        session.commit()
        session.refresh(Subscriber)
        
        return Subscriber
        
    @strawberry.mutation
    def update_Article(self, info:Info, Article_id: int, data: ArticleUpdateInput) -> Article:
        session = info.context["session"]
        Article = session.get(ArticleModel, Article_id)
        
        if not Article:
            raise Exception(f"Articleul cu ID {Article_id} nu a fost gasit.")
        update_data = strawberry.asdict(data)
        for key, value in update_data.items():
            if value is not None:
                setattr(Article, key, value)
                
        session.add(Article)
        session.commit()
        session.refresh(Article)
        
        return Article
        
    @strawberry.mutation
    def delete_NewsSource(self, info:Info, NewsSource_id: int) -> bool:
        session = info.context["session"]
        
        NewsSource = session.get(NewsSourceModel, NewsSource_id)
        if not NewsSource:
            return False

        session.delete(NewsSource)

        session.commit()
        return True
    
    @strawberry.mutation
    def delete_Subscriber(self, info:Info, Subscriber_id: int) -> bool:
        session = info.context["session"]
        
        Subscriber = session.get(SubscriberModel, Subscriber_id)
        if not Subscriber:
            return False

        session.delete(Subscriber)

        session.commit()
        return True
    
    @strawberry.mutation
    def delete_Article(self, info:Info, Article_id: int) -> bool:
        session = info.context["session"]
        
        Article = session.get(ArticleModel, Article_id)
        if not Article:
            return False

        session.delete(Article)

        session.commit()
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
