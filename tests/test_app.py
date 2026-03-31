import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    # Arrange
    # No special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) + 1


def test_signup_activity_not_found():
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_already_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_success():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # already signed up
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) - 1


def test_unregister_activity_not_found():
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_not_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not registered for this activity"}