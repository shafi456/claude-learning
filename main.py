from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from products import products, find_product, add_product

app = FastAPI()


class ProductCreate(BaseModel):
    name: str
    price: int


@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", status_code=201)
def create_product(product: ProductCreate) -> dict:
    return add_product(products, product.name, product.price)