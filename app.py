from flask import Flask, jsonify, request, send_from_directory

from data.inventory import inventory
from services.openfoodfacts import get_product_by_barcode


# ---------------------------------------------------------
# Flask application setup
# ---------------------------------------------------------

app = Flask(__name__)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def find_inventory_item(item_id):
    """
    Find an inventory item by its ID.

    Returns:
        The inventory item if found.
        None if the item does not exist.
    """
    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


def validate_price(price):
    """
    Validate and convert the price to a float.

    Returns:
        The converted price.

    Raises:
        ValueError if the price is invalid.
    """
    try:
        price = float(price)

        if price < 0:
            raise ValueError

        return price

    except (ValueError, TypeError):
        raise ValueError("Price must be a non-negative number.")


def validate_stock(stock):
    """
    Validate and convert stock to an integer.

    Returns:
        The converted stock.

    Raises:
        ValueError if the stock is invalid.
    """
    try:
        stock = int(stock)

        if stock < 0:
            raise ValueError

        return stock

    except (ValueError, TypeError):
        raise ValueError("Stock must be a non-negative integer.")


# ---------------------------------------------------------
# Home route
# ---------------------------------------------------------

@app.route("/")
def home():
    """
    Serve the inventory management web interface.
    """
    return send_from_directory("static", "index.html")


# ---------------------------------------------------------
# GET - Get all inventory items
# ---------------------------------------------------------

@app.route("/inventory", methods=["GET"])
def get_inventory():
    """
    Return all inventory items.
    """
    return jsonify(inventory), 200


# ---------------------------------------------------------
# GET - Get one inventory item
# ---------------------------------------------------------

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """
    Return one inventory item by ID.
    """

    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found."
        }), 404

    return jsonify(item), 200


# ---------------------------------------------------------
# POST - Create a new inventory item
# ---------------------------------------------------------

@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    """
    Add a new product to the inventory.
    """

    data = request.get_json()

    # Check that a JSON body was provided
    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    # -----------------------------
    # Validate product name
    # -----------------------------

    product_name = data.get("product_name", "").strip()

    if not product_name:
        return jsonify({
            "error": "Product name is required."
        }), 400

    # -----------------------------
    # Get optional product details
    # -----------------------------

    brands = data.get("brands", "").strip()
    barcode = data.get("barcode", "").strip()
    ingredients_text = data.get("ingredients_text", "").strip()

    # -----------------------------
    # Validate price
    # -----------------------------

    if "price" not in data:
        return jsonify({
            "error": "Price is required."
        }), 400

    try:
        price = validate_price(data["price"])

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    # -----------------------------
    # Validate stock
    # -----------------------------

    if "stock" not in data:
        return jsonify({
            "error": "Stock is required."
        }), 400

    try:
        stock = validate_stock(data["stock"])

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    # -----------------------------
    # Generate a new ID
    # -----------------------------

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    # -----------------------------
    # Create the new item
    # -----------------------------

    new_item = {
        "id": new_id,
        "product_name": product_name,
        "brands": brands,
        "barcode": barcode,
        "price": price,
        "stock": stock,
        "ingredients_text": ingredients_text
    }

    # Add item to inventory
    inventory.append(new_item)

    return jsonify(new_item), 201


# ---------------------------------------------------------
# PATCH - Update an inventory item
# ---------------------------------------------------------

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    """
    Update one or more fields of an inventory item.
    """

    # Find the item
    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found."
        }), 404

    # Get request data
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required."
        }), 400

    # -----------------------------
    # Update product name
    # -----------------------------

    if "product_name" in data:

        product_name = data["product_name"]

        if not isinstance(product_name, str):
            return jsonify({
                "error": "Product name must be text."
            }), 400

        product_name = product_name.strip()

        if not product_name:
            return jsonify({
                "error": "Product name cannot be empty."
            }), 400

        item["product_name"] = product_name

    # -----------------------------
    # Update brand
    # -----------------------------

    if "brands" in data:

        if not isinstance(data["brands"], str):
            return jsonify({
                "error": "Brand must be text."
            }), 400

        item["brands"] = data["brands"].strip()

    # -----------------------------
    # Update barcode
    # -----------------------------

    if "barcode" in data:

        if not isinstance(data["barcode"], str):
            return jsonify({
                "error": "Barcode must be text."
            }), 400

        item["barcode"] = data["barcode"].strip()

    # -----------------------------
    # Update ingredients
    # -----------------------------

    if "ingredients_text" in data:

        if not isinstance(data["ingredients_text"], str):
            return jsonify({
                "error": "Ingredients must be text."
            }), 400

        item["ingredients_text"] = data["ingredients_text"].strip()

    # -----------------------------
    # Update price
    # -----------------------------

    if "price" in data:

        try:
            item["price"] = validate_price(data["price"])

        except ValueError as error:
            return jsonify({
                "error": str(error)
            }), 400

    # -----------------------------
    # Update stock
    # -----------------------------

    if "stock" in data:

        try:
            item["stock"] = validate_stock(data["stock"])

        except ValueError as error:
            return jsonify({
                "error": str(error)
            }), 400

    return jsonify(item), 200


# ---------------------------------------------------------
# DELETE - Delete an inventory item
# ---------------------------------------------------------

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    """
    Delete an inventory item by ID.
    """

    item = find_inventory_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found."
        }), 404

    # Remove the item from the inventory
    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully.",
        "deleted": item
    }), 200

# ---------------------------------------------------------
# GET - Find product on OpenFoodFacts
# ---------------------------------------------------------

@app.route("/products/<barcode>", methods=["GET"])
def find_product(barcode):
    """
    Find product information on OpenFoodFacts using a barcode.
    """

    if not barcode.strip():
        return jsonify({
            "error": "Barcode is required."
        }), 400

    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found on OpenFoodFacts."
        }), 404

    return jsonify(product), 200

# ---------------------------------------------------------
# Run the application
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )