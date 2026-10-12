"""
Fixtures compartilhadas pelos testes unitários e de integração.
Os testes usam o banco de teste, e não o de desenvolvimento.
Pre requisito local: docker compose up -d
"""
import os

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://user123:123456@localhost:5433/ellpDbTest",
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ.setdefault("SECRET_KEY", "chave-de-teste")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.database import Base, engine, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import user_model  # noqa: E402,F401

@pytest.fixture(scope="session")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture()
def db_session(criar_tabelas):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
