from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import pytest

import models
from main import app

client = TestClient(app)

test_user_1 = models.User(
    firstName="Jurgen",
    lastName="Strong",
    email="jurgen@st.com",
    password="veryStrongPassword"
)

test_user_2 = models.User(
    firstName="Jurgen_2",
    lastName="Strong_2",
    email="jurgen_2@st.com",
    password="veryStrongPassword_2"
)


def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "<title>FastAPI - Swagger UI</title>" in response.text

"-------------------------"
@pytest.fixture
def mocked_database_fix(mocker):
    return mocker.patch("main.Database")


def test_all_users(mocked_database_fix: Mock):
    mocked_database_fix.return_value.find_all_users.return_value = [test_user_1, test_user_2]
    response = client.get("/users")

    expected = [
        {'email': 'jurgen@st.com', 'firstName': 'Jurgen', 'lastName': 'Strong'},
        {'email': 'jurgen_2@st.com', 'firstName': 'Jurgen_2', 'lastName': 'Strong_2'}
    ]

    assert response.status_code == 200
    assert response.json() == expected
"--------------------------"

@pytest.fixture
def mocked_database_fix_1():
    with patch("main.Database") as mocked_database:
        database_instance = Mock()
        database_instance.find_all_users.return_value = [test_user_1, test_user_2]
        database_instance.get_user_by_email.return_value = test_user_1
        mocked_database.return_value = database_instance
        yield mocked_database


def test_users_one(mocked_database_fix_1):
    response = client.get("/users/testemail@m.com")
    expected = {'email': 'jurgen@st.com', 'firstName': 'Jurgen', 'lastName': 'Strong'}

    assert response.status_code == 200
    assert response.json() == expected
    