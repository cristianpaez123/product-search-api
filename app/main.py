from fastapi import FastAPI, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "balon", "status": "active", "description": "balon de futbol"},
    {"id": 2, "name": "maleta", "status": "active", "description": "maleta de viaje"},
    {"id": 3, "name": "camisa", "status": "inactive", "description": "camisa de algodon"},
]
@app.get("/products")
def obtener_productos():
    return products

@app.get("/products/{product_id}")
def obtener_producto(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
        
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/")
def inicio():
    return {"mensaje": "Hola desde mi API"}
