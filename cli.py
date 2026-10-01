import requests


# ---------------------------------------------------------
# Flask API configuration
# ---------------------------------------------------------

BASE_URL = "http://127.0.0.1:5000"


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def make_request(method, endpoint, **kwargs):
    """
    Send a request to the Flask API and handle errors.

    Returns:
        JSON response from the API.
    """

    try:
        response = requests.request(
            method,
            f"{BASE_URL}{endpoint}",
            timeout=10,
            **kwargs
        )

        data = response.json()

        if not response.ok:
            print(f"\nError: {data.get('error', 'Request failed.')}")
            return None

        return data

    except requests.RequestException as error:
        print(f"\nCould not connect to the Flask API: {error}")
        return None


# ---------------------------------------------------------
# Display inventory
# ---------------------------------------------------------

def view_inventory():
    """Display all inventory items."""

    inventory = make_request("GET", "/inventory")

    if inventory is None:
        return

    if not inventory:
        print("\nNo inventory items found.")
        return

    print("\n" + "=" * 70)
    print("INVENTORY")
    print("=" * 70)

    for item in inventory:
        print(f"\nID: {item['id']}")
        print(f"Product: {item['product_name']}")
        print(f"Brand: {item.get('brands') or 'N/A'}")
        print(f"Barcode: {item.get('barcode') or 'N/A'}")
        print(f"Price: KSh {item['price']:.2f}")
        print(f"Stock: {item['stock']}")
        print(
            f"Ingredients: "
            f"{item.get('ingredients_text') or 'N/A'}"
        )
        print("-" * 70)


# ---------------------------------------------------------
# Add inventory item
# ---------------------------------------------------------

def add_inventory_item():
    """Add a new product to the inventory."""

    print("\n--- ADD PRODUCT ---")

    product_name = input("Product name: ").strip()
    brands = input("Brand: ").strip()
    barcode = input("Barcode: ").strip()
    price = input("Price: ").strip()
    stock = input("Stock: ").strip()
    ingredients = input("Ingredients: ").strip()

    if not product_name:
        print("Product name is required.")
        return

    if not price:
        print("Price is required.")
        return

    if not stock:
        print("Stock is required.")
        return

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    if price < 0:
        print("Price cannot be negative.")
        return

    if stock < 0:
        print("Stock cannot be negative.")
        return

    product = {
        "product_name": product_name,
        "brands": brands,
        "barcode": barcode,
        "price": price,
        "stock": stock,
        "ingredients_text": ingredients
    }

    result = make_request(
        "POST",
        "/inventory",
        json=product
    )

    if result is not None:
        print(
            f"\n{result['product_name']} "
            f"was added successfully."
        )
        print(f"Assigned ID: {result['id']}")


# ---------------------------------------------------------
# Update inventory item
# ---------------------------------------------------------

def update_inventory_item():
    """Update the price and/or stock of an inventory item."""

    print("\n--- UPDATE PRODUCT ---")

    item_id = input("Enter product ID: ").strip()

    try:
        item_id = int(item_id)
    except ValueError:
        print("Product ID must be a number.")
        return

    item = make_request(
        "GET",
        f"/inventory/{item_id}"
    )

    if item is None:
        return

    print(f"\nProduct: {item['product_name']}")
    print(f"Current price: KSh {item['price']:.2f}")
    print(f"Current stock: {item['stock']}")

    price = input(
        "New price (press Enter to keep current): "
    ).strip()

    stock = input(
        "New stock (press Enter to keep current): "
    ).strip()

    if not price and not stock:
        print("No changes were entered.")
        return

    update_data = {}

    if price:
        try:
            price = float(price)
        except ValueError:
            print("Price must be a number.")
            return

        if price < 0:
            print("Price cannot be negative.")
            return

        update_data["price"] = price

    if stock:
        try:
            stock = int(stock)
        except ValueError:
            print("Stock must be an integer.")
            return

        if stock < 0:
            print("Stock cannot be negative.")
            return

        update_data["stock"] = stock

    result = make_request(
        "PATCH",
        f"/inventory/{item_id}",
        json=update_data
    )

    if result is not None:
        print(
            f"\n{result['product_name']} "
            "was updated successfully."
        )


# ---------------------------------------------------------
# Delete inventory item
# ---------------------------------------------------------

def delete_inventory_item():
    """Delete an inventory item."""

    print("\n--- DELETE PRODUCT ---")

    item_id = input("Enter product ID: ").strip()

    try:
        item_id = int(item_id)
    except ValueError:
        print("Product ID must be a number.")
        return

    item = make_request(
        "GET",
        f"/inventory/{item_id}"
    )

    if item is None:
        return

    print(f"\nProduct: {item['product_name']}")
    print(f"Price: KSh {item['price']:.2f}")
    print(f"Stock: {item['stock']}")

    confirmation = input(
        "Are you sure you want to delete this product? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Delete cancelled.")
        return

    result = make_request(
        "DELETE",
        f"/inventory/{item_id}"
    )

    if result is not None:
        print(f"\n{result['message']}")


# ---------------------------------------------------------
# Find product on OpenFoodFacts
# ---------------------------------------------------------

def find_product_on_openfoodfacts():
    """Find product information using its barcode."""

    print("\n--- FIND PRODUCT ON OPENFOODFACTS ---")

    barcode = input("Enter barcode: ").strip()

    if not barcode:
        print("Barcode is required.")
        return

    product = make_request(
        "GET",
        f"/products/{barcode}"
    )

    if product is None:
        return

    print("\n" + "=" * 50)
    print("OPENFOODFACTS PRODUCT")
    print("=" * 50)

    print(
        f"Product: "
        f"{product.get('product_name') or 'N/A'}"
    )

    print(
        f"Brand: "
        f"{product.get('brands') or 'N/A'}"
    )

    print(
        f"Barcode: "
        f"{product.get('barcode') or 'N/A'}"
    )

    print(
        f"Ingredients: "
        f"{product.get('ingredients_text') or 'N/A'}"
    )


# ---------------------------------------------------------
# CLI menu
# ---------------------------------------------------------

def show_menu():
    """Display the main CLI menu."""

    print("\n")
    print("=" * 50)
    print("     INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. View inventory")
    print("2. Add product")
    print("3. Update product")
    print("4. Delete product")
    print("5. Find product on OpenFoodFacts")
    print("6. Exit")
    print("=" * 50)


# ---------------------------------------------------------
# Main CLI application
# ---------------------------------------------------------

def main():
    """Run the inventory management CLI."""

    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_inventory_item()

        elif choice == "3":
            update_inventory_item()

        elif choice == "4":
            delete_inventory_item()

        elif choice == "5":
            find_product_on_openfoodfacts()

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


# ---------------------------------------------------------
# Run application
# ---------------------------------------------------------

if __name__ == "__main__":
    main()