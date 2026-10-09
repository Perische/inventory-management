import pytest

from app import app


# ---------------------------------------------------------
# TEST SETUP
# ---------------------------------------------------------

@pytest.fixture
def client():
    """Create a Flask test client."""

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ---------------------------------------------------------
# GET ALL INVENTORY
# ---------------------------------------------------------

def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 404

    data = response.get_json()

    assert isinstance(data, list)


# ---------------------------------------------------------
# GET ONE INVENTORY ITEM
# ---------------------------------------------------------

def test_get_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert "product_name" in data
    assert "price" in data
    assert "stock" in data


# ---------------------------------------------------------
# GET NON-EXISTENT ITEM
# ---------------------------------------------------------

def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert "error" in data


# ---------------------------------------------------------
# CREATE INVENTORY ITEM
# ---------------------------------------------------------

def test_create_inventory_item(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Chocolate",
            "brands": "Test Brand",
            "barcode": "1234567890123",
            "price": 4.99,
            "stock": 10,
            "ingredients_text": "Cocoa, sugar, milk"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["product_name"] == "Test Chocolate"
    assert data["brands"] == "Test Brand"
    assert data["price"] == 4.99
    assert data["stock"] == 10


# ---------------------------------------------------------
# CREATE WITHOUT PRODUCT NAME
# ---------------------------------------------------------

def test_create_inventory_item_without_product_name(client):
    response = client.post(
        "/inventory",
        json={
            "brands": "Test Brand",
            "barcode": "1234567890123",
            "price": 4.99,
            "stock": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product name is required."


# ---------------------------------------------------------
# CREATE WITH INVALID PRICE
# ---------------------------------------------------------

def test_create_inventory_item_with_invalid_price(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Product",
            "price": -5,
            "stock": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "Price" in data["error"]


# ---------------------------------------------------------
# CREATE WITH INVALID STOCK
# ---------------------------------------------------------

def test_create_inventory_item_with_invalid_stock(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Product",
            "price": 5.99,
            "stock": -10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "Stock" in data["error"]


# ---------------------------------------------------------
# UPDATE INVENTORY ITEM
# ---------------------------------------------------------

def test_update_inventory_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 10.99,
            "stock": 50
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 10.99
    assert data["stock"] == 50


# ---------------------------------------------------------
# UPDATE NON-EXISTENT ITEM
# ---------------------------------------------------------

def test_update_inventory_item_not_found(client):
    response = client.patch(
        "/inventory/9999",
        json={
            "price": 10.99
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert "error" in data


# ---------------------------------------------------------
# DELETE INVENTORY ITEM
# ---------------------------------------------------------

def test_delete_inventory_item(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Delete Test Product",
            "brands": "Test Brand",
            "barcode": "9999999999999",
            "price": 5.00,
            "stock": 5
        }
    )

    assert response.status_code == 201

    created_item = response.get_json()
    item_id = created_item["id"]

    response = client.delete(
        f"/inventory/{item_id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "Inventory item deleted successfully."
    )


# ---------------------------------------------------------
# DELETE NON-EXISTENT ITEM
# ---------------------------------------------------------

def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert "error" in data
