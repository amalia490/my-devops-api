from models import NewsSource
import pytest
from sqlmodel import SQLModel, Session, create_engine
from schema import schema 

@pytest.fixture
def test_db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
def test_graphql(test_db_session):
    source = NewsSource(name="Stiri Locale", url="https://stiri-locale.ro", category="Local")
    test_db_session.add(source)
    test_db_session.commit()
    test_db_session.refresh(source)
    
    query = """
        query getNewsSourceTest($newsSourceId: Int!){
            newsSourcesById(newsSourceId: $newsSourceId){
                name
                url
                category
            }
        }
    """
    
    rez = schema.execute_sync(
        query,  
        variable_values = {"newsSourceId": source.id},
        context_value = {"session": test_db_session} 
    )
    
    assert rez.errors is None, f"Eroare GraphQL: {rez.errors}"

    result = rez.data["newsSourcesById"]
    assert result["name"] == "Stiri Locale", "Sursa nu are acelasi nume"
    assert result["url"] == "https://stiri-locale.ro", "Sursa nu are acelasi URL"
    assert result["category"] == "Local", "Sursa nu are aceeasi categorie"