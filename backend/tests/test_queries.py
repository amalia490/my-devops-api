from models import Service
import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel, Session, create_engine
from schema import schema 

@pytest.fixture
def test_db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
def test_graphql(test_db_session):
    service = Service(name="Baza de date", status="active")
    test_db_session.add(service)
    test_db_session.commit()
    test_db_session.refresh(service)
    
    query = """
        query getServiceTest($serviceIds: [Int!]!){
            servicesById(serviceIds: $serviceIds){
                name
                status
            }
        }
    """
    
    rez = schema.execute_sync(
        query,  
        variable_values = {"serviceIds": [service.id]},
        context_value = {"session": test_db_session}
    )
    assert rez.errors is None, f"Eroare GraphQL: {rez.errors}"
    result = rez.data["servicesById"]
    assert result[0]["name"] == "Baza de date", "Serviciul nu are acelasi nume"
    assert result[0]["status"] == "active", "Serviciul nu are acelasi status"