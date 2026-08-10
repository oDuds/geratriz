from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno_disciplina import AlunoDisciplina
from app.schemas.aluno_disciplina import AlunoDisciplinaCreate, AlunoDisciplinaResponse

router = APIRouter(prefix="/aluno-disciplinas", tags=["Histórico do Aluno"])


@router.post("/", response_model=AlunoDisciplinaResponse)
def registrar_status(item: AlunoDisciplinaCreate, db: Session = Depends(get_db)):
    existente = (
        db.query(AlunoDisciplina)
        .filter(
            AlunoDisciplina.aluno_id == item.aluno_id,
            AlunoDisciplina.disciplina_id == item.disciplina_id,
        )
        .first()
    )
    if existente:
        existente.status = item.status
        db.commit()
        db.refresh(existente)
        return existente

    novo = AlunoDisciplina(**item.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[AlunoDisciplinaResponse])
def listar_historico(aluno_id: int, db: Session = Depends(get_db)):
    return db.query(AlunoDisciplina).filter(AlunoDisciplina.aluno_id == aluno_id).all()