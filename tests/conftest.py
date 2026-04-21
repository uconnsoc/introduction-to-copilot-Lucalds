import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    """Test client for FastAPI app."""
    return TestClient(app, follow_redirects=False)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before and after each test."""
    original_activities = activities.copy()
    yield
    activities.clear()
    activities.update(original_activities)

@pytest.fixture
def sample_activities():
    """Sample activity data for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }