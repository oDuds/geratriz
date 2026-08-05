from fastapi import FastAPI
from app.routers import matriz

app = FastAPI(title="Geratriz")

app.include_router(matriz.router)


@app.get("/")
def root():
    return {"status": "Geratriz API rodando"}