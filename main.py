from fastapi import FastAPI

from routers import products

app = FastAPI()
app.include_router(products.router)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "version": "1.0"}