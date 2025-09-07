from TodoApp.main import app
from TodoApp.routers.auth import get_db, authenticate_user
from TodoApp.test.utils import override_get_db, TestingSessionLocal, test_user

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'qwe123', db)

    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('WrongUserName', 'qwe123', db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'WrongPassword', db)
    assert wrong_password_user is False
