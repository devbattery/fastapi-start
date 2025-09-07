from starlette import status

from TodoApp.main import app
from TodoApp.models import Todos
from TodoApp.routers.admin import get_db
from TodoApp.routers.auth import get_current_user
from TodoApp.test.utils import override_get_db, override_get_current_user, client, test_todo, TestingSessionLocal

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/api/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'complete': False, 'title': 'Learn to code!', 'description': 'Need to learn everyday!', 'id': 1, 'priority': 5,
         'owner_id': 1}]


def test_admin_delete_todo(test_todo):
    response = client.delete('/api/admin/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete('/api/admin/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
