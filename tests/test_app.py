"""
Tests for the Mergington High School API
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from app import app

client = TestClient(app)


def test_get_activities():
    """Test that the activities endpoint returns a list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_activity_has_required_fields():
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    activities = response.json()
    for name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_signup_for_activity():
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Art Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_signup_duplicate_rejected():
    """Test that duplicate signup is rejected"""
    # Sign up once
    client.post("/activities/Drama Club/signup?email=dup@mergington.edu")
    # Try to sign up again
    response = client.post(
        "/activities/Drama Club/signup?email=dup@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity():
    """Test that signing up for a nonexistent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404

