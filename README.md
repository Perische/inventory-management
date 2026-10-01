# Inventory Management System

A Flask-based Inventory Management System that allows users to manage
products, prices, stock levels, and product information.

The project includes a Flask REST API, a command-line interface (CLI),
a simple browser frontend, and integration with the OpenFoodFacts API.

---

## Features

- View all inventory items
- View a single inventory item
- Add new products
- Update product prices and stock
- Delete inventory items
- Search OpenFoodFacts using a product barcode
- Command-line interface for inventory management
- Browser-based frontend
- Input validation and error handling
- Automated tests using pytest
- Mocked external API testing

---

## Technologies Used

- Python 3.8.13
- Flask
- Requests
- Pytest
- unittest.mock
- HTML
- CSS
- JavaScript
- OpenFoodFacts API

---

## Project Structure

```text
inventory-management/
│
├── app.py
├── cli.py
│
├── data/
│   ├── __init__.py
│   └── inventory.py
│
├── services/
│   ├── __init__.py
│   └── openfoodfacts.py
│
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_inventory.py
│   └── test_openfoodfacts.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── README.md
└── venv/
