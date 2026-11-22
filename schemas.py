from pydantic import BaseModel

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