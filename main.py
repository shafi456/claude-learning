from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from products import products, find_product, add_product, available_products, under_budget

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}


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

@app.get("/products")
def list_products(in_stock: bool | None = None, max_price: int | None = None) -> list[dict]:
    
    result = products
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    return result