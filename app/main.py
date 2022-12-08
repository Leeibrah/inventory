from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional

import uvicorn

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}

@app.get("/")
def home():
        return {"message": "Inventory API Application!"}

@app.get("/product/{product_id}")
def get_product(product_id: int = Path(None, description = "The ID of the product you would like to view", gt=0)):

    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not Found!")

    return inventory[product_id]

@app.get("/product-name")
def get_product_name(name: str = Query(None, title = "Name", description = "Name of product you want to search with:", min_length=2, max_length= 10)):
    for product_id in inventory:
        if inventory[product_id].name == name:
            return inventory[product_id]
    raise HTTPException(status_code = 404, detail = "Product not Found!")


@app.post("/product/{product_id}")
def create_product(product_id: int, product: Product):
    if product_id in inventory:
        raise HTTPException(status_code = 400, detail = "Product already exist.")
    
    inventory[product_id] = product

    return inventory[product_id]


@app.put("/update-product/{product_id}")
def update_product(product_id: int, product: UpdateProduct):
    if product_id not in inventory:
        raise HTTPException(status_code = 404, detail = "Product not Found!")

    if product.name != None:
        inventory[product_id].name = product.name

    if product.price != None:
        inventory[product_id].price = product.price

    if product.brand != None:
        inventory[product_id].brand = product.brand

    return inventory[product_id]


@app.delete("/delete-product")
def delete_product(product_id: int = Query(..., description = "The ID of the product to delete.")):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not Found!")

    del inventory[product_id]

    return {"Success": "Product deleted!"}
