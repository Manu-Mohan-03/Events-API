from test.conftest import BASE_URL

import pytest
import requests
import time

def test_health_endpoint_returns_healthy():
    response = requests.get(f'{BASE_URL}/api/health')
    # Check status of the response
    assert response.status_code == 200
    # Check the response from the request contains healthy
    assert response.json()["status"] == 'healthy'

# @pytest.mark.skip
def test_user_registration():
    """For registering a new user"""
    user_data = {
      "username": f"user_{int(time.time()*1000)}",
      "password": "init1234"
    }

    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json = user_data
    )


    #check response for user creation
    assert response.status_code == 201
    # check username
    assert response.json().get("user").get("username") == user_data["username"]


def test_duplicate_user():
    user_data = {
      "username": "John",
      "password": "init1234"
    }

    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json = user_data
    )

    # Edge case on 2nd execution for the same user
    assert response.status_code == 400

def test_login_returns_jwt_token():
    user_data = {
        "username": "user_1771598004140",
        "password": "init1234"
    }
    response = requests.post(
        url = f"{BASE_URL}/api/auth/login",
        json = user_data
    )
    #check response successful
    assert response.status_code == 200
    # check access_token
    assert response.json().get("access_token")

# @pytest.mark.skip
def test_create_protected_event(auth_token):
    """To create a protected event requires auth and succeeds with token"""
    event_data = {
        "title": "Cozy Evening",
        "description": "Test Friends meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 10,
        "is_public": False,
        "requires_admin": False
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/events",
        json = event_data,
        headers = headers
    )

    # checking response code
    assert response.status_code == 201
    # check the created data from response
    assert response.json().get('title') == event_data['title']


def test_create_public_event(auth_token):
    """To create a public event requires auth and succeeds with token"""
    event_data = {
        "title": "Team Building",
        "description": "Test Team Dinner",
        "date": "2026-01-15T18:00:00",
        "location": "Pizzeria",
        "capacity": 20,
        "is_public": True,
        "requires_admin": False
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/events",
        json = event_data,
        headers = headers
    )

    # checking response code
    assert response.status_code == 201
    # check the created data from response
    assert response.json().get('title') == event_data['title']
    # to display the id
    print(response.json().get('id'))

def test_rsvp_public(is_public):
    rsvp = {
      "attending": True
    }

    response = requests.post(
        f"{BASE_URL}/api/rsvps/event/5",
        json = rsvp
    )

    # check response code for new rsvp
    if is_public:
        assert response.status_code == 201  # for new rsvp creation
    else:
        assert response.status_code == 200 # for rsvp update
    # Check if Event ID matched
    assert response.json().get("event_id") == 5

def test_create_event_no_auth():
    """Testing event creation without access token"""
    event_data = {
        "title": "Test event",
        "description": "Test Event",
        "date": "2026-01-15T18:00:00",
        "location": "Testing Room",
        "capacity": 5,
        "is_public": False,
        "requires_admin": False
    }

    response = requests.post(
        f"{BASE_URL}/api/events",
        json=event_data,
    )
    # No authorization should give 401 error code
    assert response.status_code == 401

def test_rsvp_without_token():
    rsvp = {
      "attending": True
    }

    response = requests.post(
        f"{BASE_URL}/api/rsvps/event/4", # 4 is protected
        json = rsvp
    )

    # Since no authorization response should be 400
    assert response.status_code == 401