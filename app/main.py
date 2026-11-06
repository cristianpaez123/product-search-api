from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


# --- Schemas (forma del JSON que entra y sale) ---------------------------------


class ProductCreate(BaseModel):
    """Datos que el cliente envía para crear o reemplazar un producto."""

    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: str = "active"


class Product(ProductCreate):
    """Producto tal como lo devuelve la API (incluye el id asignado por el servidor)."""

    id: int


# --- "Base de datos" en memoria (se reemplaza por PostgreSQL en el paso 3) -----

INITIAL_PRODUCTS = [
    {"id": 1, "name": "balon", "status": "active", "description": "balon de futbol"},
    {"id": 2, "name": "maleta", "status": "active", "description": "maleta de viaje"},
    {"id": 3, "name": "camisa", "status": "inactive", "description": "camisa de algodon"},
]

products: list[dict] = [product.copy() for product in INITIAL_PRODUCTS]


def find_product(product_id: int) -> dict:
    """Devuelve el producto con ese id o lanza un 404 si no existe."""
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Producto no encontrado",
    )


# --- API -----------------------------------------------------------------------

app = FastAPI(title="Product Search API", version="0.1.0")


@app.get("/")
def root():
    return {"mensaje": "Hola desde mi API"}


@app.get("/products", response_model=list[Product])
def list_products():
    return products


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    return find_product(product_id)


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate):
    new_id = max((product["id"] for product in products), default=0) + 1
    new_product = {"id": new_id, **product_in.model_dump()}
    products.append(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_in: ProductCreate):
    product = find_product(product_id)
    product.update(product_in.model_dump())
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = find_product(product_id)
    products.remove(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
