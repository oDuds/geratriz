from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.matriz import Matriz
from app.schemas.matriz import MatrizCreate, MatrizResponse
from app.security import exigir_aluno_logado

router = APIRouter(prefix="/matrizes", tags=["Matrizes"])


@router.post("/", response_model=MatrizResponse)
def criar_matriz(matriz: MatrizCreate, db: Session = Depends(get_db), aluno_id: int = Depends(exigir_aluno_logado)):
    nova_matriz = Matriz(**matriz.model_dump())
    db.add(nova_matriz)
    db.commit()
    db.refresh(nova_matriz)
    return nova_matriz


@router.get("/", response_model=list[MatrizResponse])
def listar_matrizes(db: Session = Depends(get_db)):
    return db.query(Matriz).all()


@router.get("/{matriz_id}", response_model=MatrizResponse)
def buscar_matriz(matriz_id: int, db: Session = Depends(get_db)):
    matriz = db.query(Matriz).filter(Matriz.id == matriz_id).first()
    if not matriz:
        raise HTTPException(status_code=404, detail="Matriz não encontrada")
    return matriz


@router.put("/{matriz_id}", response_model=MatrizResponse)
def atualizar_matriz(
    matriz_id: int,
    dados: MatrizCreate,
    db: Session = Depends(get_db),
    aluno_id: int = Depends(exigir_aluno_logado),
):
    matriz = db.query(Matriz).filter(Matriz.id == matriz_id).first()
    if not matriz:
        raise HTTPException(status_code=404, detail="Matriz não encontrada")

    for campo, valor in dados.model_dump().items():
        setattr(matriz, campo, valor)

    db.commit()
    db.refresh(matriz)
    return matriz


@router.delete("/{matriz_id}", status_code=204)
def deletar_matriz(
    matriz_id: int,
    db: Session = Depends(get_db),
    aluno_id: int = Depends(exigir_aluno_logado),
):
    matriz = db.query(Matriz).filter(Matriz.id == matriz_id).first()
    if not matriz:
        raise HTTPException(status_code=404, detail="Matriz não encontrada")

    db.delete(matriz)
    db.commit()