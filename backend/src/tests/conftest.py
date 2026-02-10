"""Shared pytest fixtures for all tests."""

import pytest
from app.db.schema import Base, get_session
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.factories import TransactionCategoryFactory, TransactionFactory

# Use in-memory SQLite for testing (fast and isolated)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    """Create test database engine (session-scoped)."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def session(engine):
    """Create a fresh database session for each test (function-scoped)."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Set the session on factories so they can use it
    TransactionCategoryFactory._meta.sqlalchemy_session = session
    TransactionFactory._meta.sqlalchemy_session = session

    yield session

    # Clean up
    TransactionCategoryFactory._meta.sqlalchemy_session = None
    TransactionFactory._meta.sqlalchemy_session = None
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(session):
    """Create a test client with database session override."""

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
