import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.data import get_db, Base
import app.models  

SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine_test)  