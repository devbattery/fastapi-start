import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from TodoApp.database import Base
from TodoApp.main import app
from TodoApp.models import Todos, Users
from TodoApp.routers.users import bcrypt_context

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


@pytest.fixture
def test_user():
    user = Users(
        username='devbattery',
        email='devbattery@outlook.com',
        first_name='Wonjun',
        last_name='Jeong',
        hashed_password=bcrypt_context.hash('qwe123'),
        role='admin',
        phone_number='(111)-111-1111'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
