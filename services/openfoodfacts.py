import requests


# OpenFoodFacts API endpoint
BASE_URL = "https://world.openfoodfacts.org/api/v2/product"

# Identify our application when making API requests
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student-project)"
}


def get_product_by_barcode(barcode):
    """
    Find a food product on OpenFoodFacts using its barcode.

    Returns:
        A dictionary containing product information
        if the product is found.

        None if the product does not exist.
    """

    url = f"{BASE_URL}/{barcode}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:
        print(f"OpenFoodFacts request failed: {error}")
        return None

    # OpenFoodFacts uses status 1 when a product is found
    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "barcode": barcode,
        "ingredients_text": product.get("ingredients_text", "")
    }