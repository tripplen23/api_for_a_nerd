import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)

# !Error catching
def store_not_found():
    abort(404, message="Store not found.")
def item_not_found():
    abort(404, message="Item not found.")

# TODO: Get all stores
@app.get("/store") # http://127.0.0.1:5000/store
def get_store():
    return {"stores": list(stores.values())}

# TODO: Get the specific store
@app.get("/store/<string:store_id>")
def get_store_name(store_id):
    try:
        return stores[store_id]
    except KeyError:
        store_not_found()

# TODO: Create a new specific store with empty item
@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload."
        )
        
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists.")
        
    store_id = uuid.uuid4().hex #Auto increment id number
    store = {**store_data, "id": store_id} # **passing kw args to a constructor(unpack the data in the store_data dictionary and include them in new dictionary)
    stores[store_id] = store

    return store, 201

# TODO: Delete a specific store
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        store_not_found()

# TODO: Get all the items information in the stores
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

# TODO: Get the item data of a specific store
@app.get("/item/<string:item_id>")
def get_item_in_specific_store(item_id):
    try:
        return items[item_id]
    except KeyError:
        item_not_found()

# TODO: Create item data in the specific store 
@app.post("/item")
def create_item():
    item_data = request.get_json()
    '''
    Here not only we need to validate data exists,
    but also what type of data. Price should be a float,
    for example.
    '''
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message = "Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload"
        )
    # We cannot add the same item twice
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exists.")

    # Check that the store that we are trying to add this item to, also exists
    if item_data["store_id"] not in stores:
        store_not_found()

    item_id = uuid.uuid4().hex # Create item id
    item = {**item_data, "id": item_id} # Save it to items dictionary
    items[item_id] = item # places it in our items dictionary

    return item, 201

# TODO: Delete the item data from the specific store
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        item_not_found()

# TODO: Update the item data in the specific store
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")

    try:
        item = items[item_id]
        item.update(item_data)  # New dictionary update operator

        return item
    except KeyError:
        item_not_found()