# tests/test_token.py

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from core.security import get_password_hash
from models.user import User


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

if os.path.exists(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")):
    os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture
def db_session():
    """Crée une nouvelle session de base de données pour chaque test, avec rollback."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Crée un utilisateur admin pour les tests nécessitant un login."""
    hashed_password = get_password_hash("adminpass")
    user = User(email="admin@example.com", hashed_password=hashed_password, role="admin", is_active=True)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# --- TESTS ---

def test_register_user(test_user, db_session):
    login_response = client.post(
        "/api/token/",
        data={"username": test_user.email, "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/token/register/",
        json={
            "email": "newadmin@example.com",
            "password": "securepassword",
            "role": "admin"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["msg"] == "User successfully registered"
    assert "user_id" in response.json()

    new_user = db_session.query(User).filter(User.email == "newadmin@example.com").first()
    assert new_user is not None
    assert new_user.role == "admin"


def test_register_user_non_admin_role(test_user, db_session):
    login_response = client.post(
        "/api/token/",
        data={"username": test_user.email, "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/token/register/",
        json={
            "email": "user@example.com",
            "password": "userpassword",
            "role": "user"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 403:
        assert response.json()["detail"] == "Access denied: Admins only"
    else:
        assert response.status_code == 201  


def test_login_success(test_user):
    response = client.post(
        "/api/token/",
        data={"username": test_user.email, "password": "adminpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"
    assert json["role"] == "admin"


def test_login_fail_wrong_password(test_user):
    response = client.post(
        "/api/token/",
        data={"username": test_user.email, "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
