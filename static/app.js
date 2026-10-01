// -----------------------------------------------------------------------------
// HELPER FUNCTION - API REQUESTS
// -----------------------------------------------------------------------------

async function requestJSON(url, options = {}) {

    const response = await fetch(url, options);

    let data;

    try {
        data = await response.json();

    } catch (error) {

        data = {
            error: `Server returned ${response.status} without valid JSON.`
        };
    }


    if (!response.ok) {

        throw new Error(
            data.error ||
            `Request failed with status ${response.status}.`
        );
    }


    return data;
}


// -----------------------------------------------------------------------------
// ERROR HANDLING
// -----------------------------------------------------------------------------

function showError(message) {

    const errorBox =
        document.getElementById("errorBox");


    errorBox.textContent = message;

    errorBox.classList.remove("hidden");
}


function clearError() {

    const errorBox =
        document.getElementById("errorBox");


    errorBox.textContent = "";

    errorBox.classList.add("hidden");
}


async function runSafely(action) {

    clearError();

    try {

        await action();

    } catch (error) {

        showError(error.message);
    }
}


// -----------------------------------------------------------------------------
// READ - GET ALL INVENTORY
// Endpoint: GET /inventory
// -----------------------------------------------------------------------------

async function loadInventory() {

    const inventory =
        await requestJSON("/inventory");


    const container =
        document.getElementById("inventoryList");


    // Show message if there are no products
    if (inventory.length === 0) {

        container.innerHTML = `
            <p>No inventory items found.</p>
        `;

        return;
    }


    // Create the spreadsheet-style inventory table
    container.innerHTML = `

        <table class="inventory-table">

            <thead>

                <tr>

                    <th>ID</th>

                    <th>Product Name</th>

                    <th>Brand</th>

                    <th>Barcode</th>

                    <th>Price</th>

                    <th>Stock</th>

                    <th>Ingredients</th>

                    <th>Actions</th>

                </tr>

            </thead>


            <tbody>

                ${inventory.map(item => `

                    <tr>

                        <td class="id">
                            ${item.id}
                        </td>


                        <td class="product-name">
                            ${item.product_name}
                        </td>


                        <td>
                            ${item.brands || "N/A"}
                        </td>


                        <td>
                            ${item.barcode || "N/A"}
                        </td>


                        <td class="price">
                            KSh ${Number(item.price).toFixed(2)}
                        </td>


                        <td class="stock">
                            ${item.stock}
                        </td>


                        <td>
                            ${item.ingredients_text || "N/A"}
                        </td>


                        <td class="actions">

                            <button
                                data-edit-id="${item.id}">
                                Edit
                            </button>


                            <button
                                class="danger"
                                data-delete-id="${item.id}">
                                Delete
                            </button>

                        </td>

                    </tr>

                `).join("")}

            </tbody>

        </table>
    `;
}


// -----------------------------------------------------------------------------
// CREATE - ADD NEW INVENTORY ITEM
// Endpoint: POST /inventory
// -----------------------------------------------------------------------------

async function createInventoryItem() {

    // Get form values
    const productName =
        document
            .getElementById("productName")
            .value
            .trim();


    const brands =
        document
            .getElementById("brands")
            .value
            .trim();


    const barcode =
        document
            .getElementById("barcode")
            .value
            .trim();


    const price =
        document
            .getElementById("price")
            .value;


    const stock =
        document
            .getElementById("stock")
            .value;


    const ingredients =
        document
            .getElementById("ingredients")
            .value
            .trim();


    // Validate product name
    if (!productName) {

        throw new Error(
            "Product name is required."
        );
    }


    // Validate price
    if (price === "") {

        throw new Error(
            "Price is required."
        );
    }


    // Validate stock
    if (stock === "") {

        throw new Error(
            "Stock is required."
        );
    }


    // Send POST request to Flask
    await requestJSON("/inventory", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            product_name: productName,

            brands: brands,

            barcode: barcode,

            price: price,

            stock: stock,

            ingredients_text: ingredients

        })

    });


    // Clear form
    document.getElementById("productName").value = "";

    document.getElementById("brands").value = "";

    document.getElementById("barcode").value = "";

    document.getElementById("price").value = "";

    document.getElementById("stock").value = "";

    document.getElementById("ingredients").value = "";


    // Refresh inventory
    await loadInventory();
}


// -----------------------------------------------------------------------------
// UPDATE - SHOW EDIT FORM
// Endpoint: GET /inventory/<id>
// -----------------------------------------------------------------------------

async function showEditForm(id) {

    // Get the product
    const item =
        await requestJSON(`/inventory/${id}`);


    // Store product ID
    document.getElementById("editItemId").value =
        item.id;


    // Show product name
    document.getElementById("editProductName").textContent =
        item.product_name;


    // Fill current price
    document.getElementById("editPrice").value =
        item.price;


    // Fill current stock
    document.getElementById("editStock").value =
        item.stock;


    // Show update section
    document
        .getElementById("editForm")
        .classList
        .remove("hidden");


    // Scroll to the update section
    document
        .getElementById("editForm")
        .scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
}


// -----------------------------------------------------------------------------
// UPDATE - PATCH INVENTORY ITEM
// Endpoint: PATCH /inventory/<id>
// -----------------------------------------------------------------------------

async function updateInventoryItem(id) {

    const price =
        document
            .getElementById("editPrice")
            .value;


    const stock =
        document
            .getElementById("editStock")
            .value;


    // Make sure something was changed
    if (price === "" && stock === "") {

        throw new Error(
            "Enter a new price or stock quantity."
        );
    }


    // Build update object
    const updateData = {};


    if (price !== "") {

        updateData.price = price;
    }


    if (stock !== "") {

        updateData.stock = stock;
    }


    // Send PATCH request
    await requestJSON(
        `/inventory/${id}`,
        {

            method: "PATCH",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(updateData)

        }
    );


    // Hide update form
    hideEditForm();


    // Refresh inventory
    await loadInventory();
}


// -----------------------------------------------------------------------------
// HIDE EDIT FORM
// -----------------------------------------------------------------------------

function hideEditForm() {

    document
        .getElementById("editForm")
        .classList
        .add("hidden");


    // Clear edit fields
    document.getElementById("editPrice").value = "";

    document.getElementById("editStock").value = "";

    document.getElementById("editProductName").textContent = "";
}


// -----------------------------------------------------------------------------
// DELETE - DELETE INVENTORY ITEM
// Endpoint: DELETE /inventory/<id>
// -----------------------------------------------------------------------------

async function deleteInventoryItem(id) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this inventory item?"
        );


    if (!confirmed) {

        return;
    }


    // Send DELETE request
    await requestJSON(
        `/inventory/${id}`,
        {
            method: "DELETE"
        }
    );


    // Refresh inventory
    await loadInventory();
}


// -----------------------------------------------------------------------------
// OPENFOODFACTS - FIND PRODUCT
// Endpoint: GET /products/<barcode>
// -----------------------------------------------------------------------------

async function findProductOnOpenFoodFacts() {

    // Get barcode from search field
    const barcode =
        document
            .getElementById("searchBarcode")
            .value
            .trim();


    // Validate barcode
    if (!barcode) {

        throw new Error(
            "Please enter a barcode."
        );
    }


    // Ask Flask to search OpenFoodFacts
    const product =
        await requestJSON(
            `/products/${encodeURIComponent(barcode)}`
        );


    // Get result container
    const container =
        document.getElementById("externalProduct");


    // Display product information
    container.innerHTML = `

        <div class="status">

            <h3>Product Found</h3>


            <p>
                <strong>Product:</strong>
                ${product.product_name || "N/A"}
            </p>


            <p>
                <strong>Brand:</strong>
                ${product.brands || "N/A"}
            </p>


            <p>
                <strong>Barcode:</strong>
                ${product.barcode || barcode}
            </p>


            <p>
                <strong>Ingredients:</strong>
                ${product.ingredients_text || "N/A"}
            </p>

        </div>
    `;
}


// -----------------------------------------------------------------------------
// BUTTON EVENTS
// -----------------------------------------------------------------------------

// Refresh inventory
document
    .getElementById("loadInventory")
    .addEventListener(
        "click",
        () => runSafely(loadInventory)
    );


// -----------------------------------------------------------------------------
// ADD PRODUCT FORM
// -----------------------------------------------------------------------------

document
    .getElementById("addProductForm")
    .addEventListener(
        "submit",
        event => {

            event.preventDefault();

            runSafely(createInventoryItem);
        }
    );


// -----------------------------------------------------------------------------
// SAVE PRODUCT CHANGES
// -----------------------------------------------------------------------------

document
    .getElementById("updateProductButton")
    .addEventListener(
        "click",
        () => {

            const id =
                document
                    .getElementById("editItemId")
                    .value;


            runSafely(
                () => updateInventoryItem(
                    Number(id)
                )
            );
        }
    );


// -----------------------------------------------------------------------------
// CANCEL EDIT
// -----------------------------------------------------------------------------

document
    .getElementById("cancelEdit")
    .addEventListener(
        "click",
        hideEditForm
    );


// -----------------------------------------------------------------------------
// INVENTORY TABLE BUTTONS
// -----------------------------------------------------------------------------

document
    .getElementById("inventoryList")
    .addEventListener(
        "click",
        event => {

            const editId =
                event.target.dataset.editId;


            const deleteId =
                event.target.dataset.deleteId;


            // Edit button
            if (editId) {

                runSafely(
                    () => showEditForm(
                        Number(editId)
                    )
                );

                return;
            }


            // Delete button
            if (deleteId) {

                runSafely(
                    () => deleteInventoryItem(
                        Number(deleteId)
                    )
                );
            }

        }
    );


// -----------------------------------------------------------------------------
// OPENFOODFACTS SEARCH BUTTON
// -----------------------------------------------------------------------------

document
    .getElementById("searchProductButton")
    .addEventListener(
        "click",
        () => runSafely(
            findProductOnOpenFoodFacts
        )
    );


// -----------------------------------------------------------------------------
// LOAD INVENTORY WHEN PAGE OPENS
// -----------------------------------------------------------------------------

runSafely(loadInventory);