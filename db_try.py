import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


def find_product(conn: psycopg.Connection, product_id: int) -> dict | None:    
    return conn.execute(
        "SELECT id, name, price, in_stock FROM products WHERE id = %s",
        (product_id,),
    ).fetchone()


def add_product(conn: psycopg.Connection, name: str, price: int) -> dict:
    return conn.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) "
        "RETURNING id, name, price, in_stock",
        (name, price),
    ).fetchone()

if __name__ == "__main__":
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        print(find_product(conn, 3))
        print(find_product(conn, 99))
        print(add_product(conn, "Webcam", 0))