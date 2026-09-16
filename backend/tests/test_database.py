from models import NewsSource 
import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel, Session, create_engine

from schema import schema 

def test_newssource():
    source = NewsSource(
        name="Stiri Nationale",
        url="https://stiri-nationale.ro", 
        category="General"
    )
    assert source.name == "Stiri Nationale", "E gresit numele sursei"
    assert source.url == "https://stiri-nationale.ro", "Nu e corect URL-ul"
    assert source.category == "General", "Nu e corecta categoria"
    assert source.id is None, "Nu e none"
    
def test_newssource_fails():
    with pytest.raises(ValidationError):
        # Missing the required 'url' field
        invalid_data = {"name": "Stiri Nationale"} 
        NewsSource.model_validate(invalid_data)