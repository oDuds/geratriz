from fastapi import FastAPI
from app.routers import matriz, disciplina, oferta, pre_requisito

app = FastAPI(title="Geratriz")

app.include_router(matriz.router)
app.include_router(disciplina.router)
app.include_router(oferta.router)
app.include_router(pre_requisito.router)


@app.get("/")
def root():
    return {"status": "Geratriz API rodando"}