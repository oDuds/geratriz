from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import matriz, disciplina, oferta, pre_requisito, aluno, aluno_disciplina, grade

app = FastAPI(title="Geratriz")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matriz.router)
app.include_router(disciplina.router)
app.include_router(oferta.router)
app.include_router(pre_requisito.router)
app.include_router(aluno.router)
app.include_router(aluno_disciplina.router)
app.include_router(grade.router)


@app.get("/")
def root():
    return {"status": "Geratriz API rodando"}