from models import Incident 
import pytest
from pydantic import ValidationError

def test_incident():
    incident = Incident(
        service_id = 1,
        description="Baza de date a picat", 
        resolved=False
    )
    assert incident.service_id == 1, "E gresit service_id-ul"
    assert incident.description == "Baza de date a picat", "Nu e corecta descrierea"
    assert incident.resolved is False, "Nu e false"
    assert incident.id is None, "Nu e none"
    
def test_incident_fails():
    with pytest.raises(ValidationError):
        invalid_data = {"resolved": False} 
        Incident.model_validate(invalid_data)
        
