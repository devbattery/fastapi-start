import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from TodoApp.database import Base
from TodoApp.main import app
from TodoApp.models import Todos
from TodoApp.routers.auth import get_current_user
from TodoApp.routers.todos import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'redhood', 'id': 1, 'user_role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'complete': False, 'title': 'Learn to code!', 'description': 'Need to learn everyday!', 'id': 1,
         'priority': 5, 'owner_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/api/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Learn to code!', 'description': 'Need to learn everyday!',
                               'id': 1, 'priority': 5, 'owner_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/api/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}
