from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from products import products, find_product, add_product, available_products, under_budget

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "version": "1.0"}


class ProductCreate(BaseModel):
    name: str
    price: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    in_stock: bool | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    in_stock: bool


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int) -> None:
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products.remove(product)


@app.patch("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate):
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    changes = data.model_dump(exclude_unset=True)
    product.update(changes)
    return product


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", status_code=201, response_model=ProductOut)
def create_product(product: ProductCreate):
    return add_product(products, product.name, product.price)

@app.get("/products", response_model=list[ProductOut])
def list_products(in_stock: bool | None = None, max_price: int | None = None):
    
    result = products
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    return result