# Session 1 practice: working with lists of dicts
products = [
    {"id": 1, "name": "Keyboard", "price": 1500, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 600, "in_stock": False},
    {"id": 3, "name": "Monitor", "price": 15000, "in_stock": True},
    {"id": 4, "name": "Headphones", "price": 2500, "in_stock": True},
]

def find_product(products: list[dict], product_id: int) -> list[dict] | None:
    for p in products:
        if p["id"] == product_id:
            return p
    return None

def available_products(products: list[dict]) -> list[dict]:
    return [p for p in products if p["in_stock"]]

def under_budget(products: list[dict], max_price: int) -> list[dict]:
    return [p for p in products if p["price"] <= max_price]

def add_product(products: list[dict], name: str, price: int) -> dict:
    new_product = {}
    new_product["id"] = max(p["id"] for p in products) + 1
    new_product["name"] = name
    new_product["price"] = price
    new_product["in_stock"] = True
    products.append(new_product)
    return new_product

if __name__ == "__main__":
    print(find_product(products, 3))
    print(find_product(products, 99))
    print(available_products(products))
    print(under_budget(products, 2000))