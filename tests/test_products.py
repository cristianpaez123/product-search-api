import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_products():
    """Cada prueba arranca con los 3 productos iniciales."""
    main.products[:] = [product.copy() for product in main.INITIAL_PRODUCTS]


def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_product():
    response = client.get("/products/2")
    assert response.status_code == 200
    assert response.json()["name"] == "maleta"


def test_get_product_not_found():
    response = client.get("/products/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Producto no encontrado"}


def test_get_product_invalid_id():
    response = client.get("/products/abc")
    assert response.status_code == 422


def test_create_product():
    response = client.post("/products", json={"name": "zapatos"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "name": "zapatos",
        "description": None,
        "status": "active",
    }
    assert len(client.get("/products").json()) == 4


def test_create_product_without_name():
    response = client.post("/products", json={"description": "sin nombre"})
    assert response.status_code == 422


def test_create_product_with_empty_name():
    response = client.post("/products", json={"name": ""})
    assert response.status_code == 422


def test_update_product():
    response = client.put(
        "/products/1",
        json={"name": "balon pro", "description": "balon profesional", "status": "active"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "balon pro"
    assert client.get("/products/1").json()["name"] == "balon pro"


def test_update_product_not_found():
    response = client.put("/products/99", json={"name": "x"})
    assert response.status_code == 404


def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 204
    assert client.get("/products/1").status_code == 404


def test_delete_product_not_found():
    response = client.delete("/products/99")
    assert response.status_code == 404
