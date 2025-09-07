from starlette import status

from TodoApp.main import app
from TodoApp.routers.admin import get_db
from TodoApp.routers.auth import get_current_user
from TodoApp.test.utils import override_get_db, override_get_current_user, client, test_todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/api/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'complete': False, 'title': 'Learn to code!', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5,
         'owner_id': 1}]
