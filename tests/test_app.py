import pytest
from fastapi.testclient import TestClient
from src.app import app

# Initial activities data for resetting
INITIAL_ACTIVITIES = {
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
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Train for competitive soccer matches and learn teamwork on the field",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Practice swimming techniques, drills, and endurance in the school pool",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu", "liam@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and digital art in a creative studio setting",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Develop acting, stagecraft, and production skills for school performances",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Society": {
        "description": "Research current issues and practice persuasive speaking in team debates",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ryan@mergington.edu", "zoe@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Build problem-solving skills through science challenges and competitions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
    }
}

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities global variable before each test."""
    from src import app
    app.activities = INITIAL_ACTIVITIES.copy()

def test_root_redirect(client):
    """Test that root endpoint serves the index.html."""
    # Arrange
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert "Mergington High School Activities" in response.text

def test_get_activities(client):
    """Test retrieving all activities."""
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Number of activities
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]

def test_signup_successful(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

def test_signup_activity_not_found(client):
    """Test signup for non-existent activity."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_signup_duplicate_participant(client):
    """Test signup when student is already signed up."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()

def test_remove_participant_successful(client):
    """Test successful removal of a participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

def test_remove_participant_activity_not_found(client):
    """Test removal from non-existent activity."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_remove_participant_not_found(client):
    """Test removal of participant not in activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "notparticipant@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()