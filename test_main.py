from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from main import app, Base, get_db
from sqlalchemy.orm import sessionmaker
import pytest, models
client = TestClient(app) 

TEST_DATABASE_URL = "sqlite:///./test_items.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)




@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_get_items():
    response = client.get("/items")
    assert response.status_code ==  200
    assert isinstance(response.json(), list)


def test_get_item_not_found():
    response = client.get("/items/484")
    assert response.status_code == 404
    assert response.json() == {"detail" : "Item not found"}

def test_get_item():
    create_reponse = client.post(
        "/items", 
        json={"name": "item_name", "description": "item description", "price": 45}
    )
    assert create_reponse.status_code == 200
    item_id = create_reponse.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == "item_name"

def test_create_item():
    response = client.post(
        "/items", 
        json={"name": "create item", "description": "create item description", "price": 451}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "create item"
    assert response.json()["description"] == "create item description"
    assert response.json()["price"] == 451
    assert "id" in response.json()

def test_put_item():
    create_reponse = client.post(
        "/items", 
        json={"name": "x", "description": "update item description", "price": 452}
    )

    assert create_reponse.status_code == 200
    item_id = create_reponse.json()["id"]
    response = client.put(
        f"/items/{item_id}", 
        json={"name": "update_name new", "description": "new update item description", "price": 453}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "update_name new"
    assert response.json()["description"] == "new update item description"
    assert response.json()["price"] == 453


def test_put_item():
    create_reponse = client.post(
        "/items", 
        json={"name": "x", "description": "update item description", "price": 452}
    )

    assert create_reponse.status_code == 200
    item_id = create_reponse.json()["id"]
    response = client.put(
        f"/items/{item_id}", 
        json={"name": "update_name new", "description": "new update item description", "price": 453}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "update_name new"
    assert response.json()["description"] == "new update item description"
    assert response.json()["price"] == 453

def test_patch_item():

    create_reponse = client.post(
        "/items", 
        json={"name": "patch", "description": "patch description 0.1", "price": 456}
    )

    assert create_reponse.status_code == 200
    item_id = create_reponse.json()["id"]
    response = client.patch(
        f"/items/{item_id}", 
        json={"name": "patch update 0.1"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "patch update 0.1"
    assert response.json()["description"] == "patch description 0.1"
    assert response.json()["price"] == 456

def test_delete_item():

    create_reponse = client.post(
        "/items", 
        json={"name": "delete", "description": "delete description 0.1", "price": 457}
    )

    assert create_reponse.status_code == 200
    item_id = create_reponse.json()["id"]
    response = client.delete(
        f"/items/{item_id}"
    )
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

def test_create_item_missing_column():
    response = client.post(
        "/items", 
        json={"name": "create item", "description": "create item description"}
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "price"]

def test_create_item_invalid_datatype():
    response = client.post(
        "/items", 
        json={"name": "create item", "description": "create item description", "price": "string"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "price"]
