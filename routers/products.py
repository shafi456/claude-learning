from fastapi import APIRouter, HTTPException

from schemas import ProductCreate, ProductOut, ProductUpdate
from store import add_product, find_product, products

router = APIRouter(prefix="/products", tags=["products"])

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int) -> None:
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products.remove(product)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate):
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    changes = data.model_dump(exclude_unset=True)
    product.update(changes)
    return product


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    product = find_product(products, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", status_code=201, response_model=ProductOut)
def create_product(product: ProductCreate):
    return add_product(products, product.name, product.price)

@router.get("", response_model=list[ProductOut])
def list_products(in_stock: bool | None = None, max_price: int | None = None):
    
    result = products
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    return result