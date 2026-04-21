import pytest
from src.app import activities

def test_get_root_redirect(client):
    """Test GET / redirects to static index."""
    # Arrange
    # (client fixture provides TestClient)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client):
    """Test GET /activities returns all activities."""
    # Arrange
    # (reset_activities fixture ensures clean state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Should have activities
    # Check structure of first activity
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)

@pytest.mark.parametrize("activity_name,email,expected_status", [
    ("Chess Club", "newstudent@mergington.edu", 200),
    ("Chess Club", "michael@mergington.edu", 400),  # Already signed up
    ("NonExistent Activity", "student@mergington.edu", 404),
])
def test_post_signup(client, activity_name, email, expected_status):
    """Test POST /activities/{name}/signup with various scenarios."""
    # Arrange
    # (reset_activities ensures initial state)

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        # Verify participant was added
        assert email in activities[activity_name]["participants"]
    elif expected_status == 400:
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]
    elif expected_status == 404:
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]

@pytest.mark.parametrize("activity_name,email,expected_status", [
    ("Chess Club", "michael@mergington.edu", 200),  # Existing participant
    ("Chess Club", "nonexistent@mergington.edu", 404),  # Not signed up
    ("NonExistent Activity", "student@mergington.edu", 404),
])
def test_delete_participant(client, activity_name, email, expected_status):
    """Test DELETE /activities/{name}/participants/{email} with various scenarios."""
    # Arrange
    # (reset_activities ensures initial state)

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        # Verify participant was removed
        assert email not in activities[activity_name]["participants"]
    elif expected_status == 404:
        data = response.json()
        assert "detail" in data
        if "Activity not found" in data["detail"]:
            pass  # Activity doesn't exist
        else:
            assert "Participant not found" in data["detail"]