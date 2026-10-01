from unittest.mock import patch

import cli


# ---------------------------------------------------------
# TEST VIEW INVENTORY
# ---------------------------------------------------------

@patch("cli.make_request")
def test_view_inventory(mock_request, capsys):

    mock_request.return_value = [
        {
            "id": 1,
            "product_name": "Nutella",
            "brands": "Nutella, Ferrero",
            "barcode": "3017620422003",
            "price": 8.50,
            "stock": 20,
            "ingredients_text": "Sugar, palm oil, hazelnuts"
        }
    ]

    cli.view_inventory()

    captured = capsys.readouterr()

    assert "Nutella" in captured.out
    assert "Nutella, Ferrero" in captured.out
    assert "3017620422003" in captured.out


# ---------------------------------------------------------
# TEST ADD PRODUCT
# ---------------------------------------------------------

@patch("cli.make_request")
@patch("builtins.input")
def test_add_inventory_item(mock_input, mock_request):

    mock_input.side_effect = [
        "Nutella",
        "Nutella, Ferrero",
        "3017620422003",
        "8.50",
        "20",
        "Sugar, palm oil, hazelnuts"
    ]

    mock_request.return_value = {
        "id": 4,
        "product_name": "Nutella",
        "brands": "Nutella, Ferrero",
        "barcode": "3017620422003",
        "price": 8.50,
        "stock": 20,
        "ingredients_text": "Sugar, palm oil, hazelnuts"
    }

    cli.add_inventory_item()

    mock_request.assert_called_once()

    call_args = mock_request.call_args

    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "/inventory"

    assert call_args[1]["json"]["product_name"] == "Nutella"
    assert call_args[1]["json"]["price"] == 8.50
    assert call_args[1]["json"]["stock"] == 20


# ---------------------------------------------------------
# TEST UPDATE PRODUCT
# ---------------------------------------------------------

@patch("cli.make_request")
@patch("builtins.input")
def test_update_inventory_item(mock_input, mock_request):

    mock_input.side_effect = [
        "1",
        "10.00",
        "30"
    ]

    mock_request.side_effect = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "price": 5.99,
            "stock": 20
        },
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "price": 10.00,
            "stock": 30
        }
    ]

    cli.update_inventory_item()

    assert mock_request.call_count == 2

    update_call = mock_request.call_args_list[1]

    assert update_call[0][0] == "PATCH"
    assert update_call[0][1] == "/inventory/1"

    assert update_call[1]["json"]["price"] == 10.00
    assert update_call[1]["json"]["stock"] == 30


# ---------------------------------------------------------
# TEST DELETE PRODUCT
# ---------------------------------------------------------

@patch("cli.make_request")
@patch("builtins.input")
def test_delete_inventory_item(mock_input, mock_request):

    mock_input.side_effect = [
        "1",
        "y"
    ]

    mock_request.side_effect = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "price": 5.99,
            "stock": 20
        },
        {
            "message": "Inventory item deleted successfully."
        }
    ]

    cli.delete_inventory_item()

    assert mock_request.call_count == 2

    delete_call = mock_request.call_args_list[1]

    assert delete_call[0][0] == "DELETE"
    assert delete_call[0][1] == "/inventory/1"


# ---------------------------------------------------------
# TEST OPENFOODFACTS SEARCH
# ---------------------------------------------------------

@patch("cli.make_request")
@patch("builtins.input")
def test_find_product_on_openfoodfacts(
    mock_input,
    mock_request,
    capsys
):

    mock_input.return_value = "3017620422003"

    mock_request.return_value = {
        "product_name": "Nutella",
        "brands": "Nutella, Ferrero",
        "barcode": "3017620422003",
        "ingredients_text": "Sugar, palm oil, hazelnuts"
    }

    cli.find_product_on_openfoodfacts()

    captured = capsys.readouterr()

    assert "Nutella" in captured.out
    assert "Nutella, Ferrero" in captured.out
    assert "3017620422003" in captured.out


# ---------------------------------------------------------
# TEST INVALID PRODUCT ID
# ---------------------------------------------------------

@patch("builtins.input")
def test_update_inventory_invalid_id(mock_input, capsys):

    mock_input.return_value = "abc"

    cli.update_inventory_item()

    captured = capsys.readouterr()

    assert "Product ID must be a number." in captured.out
