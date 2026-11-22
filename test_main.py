from fastapi.testclient import TestClient

from main import app

import copy

import pytest

from store import products

ORIGINAL_PRODUCTS = copy.deepcopy(products)

@pytest.fixture(autouse = True)
def reset_products():
    products[:] = copy.deepcopy(ORIGINAL_PRODUCTS)

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0"}

def test_get_product():
    response = client.get("/products/3")
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor"

def test_get_missing_product():
    response = client.get("/products/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product():
    response = client.post("/products", json={"name": "Laptop", "price": 99})
    assert response.status_code == 201
    assert response.json()["id"] == 5

def test_create_invalid_product():
    response = client.post("/products", json={"name": "Pendrive", "price": "cheap"})
    assert response.status_code == 422

def test_update_product():
    response = client.patch("/products/1", json={"price": 1600})
    assert response.status_code == 200
    assert response.json()["price"] == 1600
    assert response.json()["name"] == "Keyboard"

def test_delete_product():
    response_delete = client.delete("/products/2")
    assert response_delete.status_code == 204
    response_get = client.get("/products/2")
    assert response_get.status_code == 404

def test_get_product_hides_supplier_cost():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert "supplier_cost" not in response.json()

def test_list_products_filters_out_of_stock():
    response = client.get("/products?in_stock=false")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2

