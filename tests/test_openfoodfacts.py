import requests
from unittest.mock import patch, Mock

from services.openfoodfacts import get_product_by_barcode


# ---------------------------------------------------------
# TEST SUCCESSFUL PRODUCT LOOKUP
# ---------------------------------------------------------

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_success(mock_get):

    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Nutella, Ferrero",
            "ingredients_text": (
                "Sugar, palm oil, hazelnuts 13%, "
                "skimmed milk powder"
            )
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_product_by_barcode("3017620422003")

    assert result["product_name"] == "Nutella"
    assert result["brands"] == "Nutella, Ferrero"
    assert result["barcode"] == "3017620422003"
    assert "Sugar" in result["ingredients_text"]

    mock_get.assert_called_once()


# ---------------------------------------------------------
# TEST PRODUCT NOT FOUND
# ---------------------------------------------------------

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_not_found(mock_get):

    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0,
        "status_verbose": "product not found"
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_product_by_barcode("9999999999999")

    assert result is None

    mock_get.assert_called_once()


# ---------------------------------------------------------
# TEST API REQUEST FAILURE
# ---------------------------------------------------------

@patch("services.openfoodfacts.requests.get")
def test_get_product_by_barcode_request_error(mock_get):

    mock_get.side_effect = requests.RequestException(
        "Connection failed"
    )

    result = get_product_by_barcode("3017620422003")

    assert result is None
