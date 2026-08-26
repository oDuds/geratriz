from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.disciplina import Disciplina
from app.schemas.disciplina import DisciplinaCreate, DisciplinaResponse
from app.security import exigir_aluno_logado

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])


@router.post("/", response_model=DisciplinaResponse)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db), aluno_id: int = Depends(exigir_aluno_logado)):
    nova_disciplina = Disciplina(**disciplina.model_dump())
    db.add(nova_disciplina)
    db.commit()
    db.refresh(nova_disciplina)
    return nova_disciplina


@router.get("/", response_model=list[DisciplinaResponse])
def listar_disciplinas(matriz_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Disciplina)
    if matriz_id is not None:
        query = query.filter(Disciplina.matriz_id == matriz_id)
    return query.all()


@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def buscar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina


@router.put("/{disciplina_id}", response_model=DisciplinaResponse)
def atualizar_disciplina(
    disciplina_id: int,
    dados: DisciplinaCreate,
    db: Session = Depends(get_db),
    aluno_id: int = Depends(exigir_aluno_logado),
):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    for campo, valor in dados.model_dump().items():
        setattr(disciplina, campo, valor)

    db.commit()
    db.refresh(disciplina)
    return disciplina


@router.delete("/{disciplina_id}", status_code=204)
def deletar_disciplina(
    disciplina_id: int,
    db: Session = Depends(get_db),
    aluno_id: int = Depends(exigir_aluno_logado),
):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    db.delete(disciplina)
    db.commit()