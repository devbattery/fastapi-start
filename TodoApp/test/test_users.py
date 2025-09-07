from starlette import status

from TodoApp.main import app
from TodoApp.routers.auth import get_current_user
from TodoApp.routers.users import get_db
from TodoApp.test.utils import override_get_db, override_get_current_user, client, test_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/api/users/me')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'devbattery'
    assert response.json()['email'] == 'devbattery@outlook.com'
    assert response.json()['first_name'] == 'Wonjun'
    assert response.json()['last_name'] == 'Jeong'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'
