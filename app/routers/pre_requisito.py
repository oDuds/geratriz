from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pre_requisito import PreRequisito
from app.schemas.pre_requisito import PreRequisitoCreate, PreRequisitoResponse
from app.security import exigir_aluno_logado

router = APIRouter(prefix="/pre-requisitos", tags=["Pré-requisitos"])


@router.post("/", response_model=PreRequisitoResponse)
def criar_pre_requisito(pre_requisito: PreRequisitoCreate, db: Session = Depends(get_db), aluno_id: int = Depends(exigir_aluno_logado)):
    if pre_requisito.tipo == "direto" and not pre_requisito.disciplina_requisito_id:
        raise HTTPException(
            status_code=400,
            detail="Requisito do tipo 'direto' precisa de disciplina_requisito_id",
        )
    if pre_requisito.tipo == "acumulo" and pre_requisito.valor_minimo is None:
        raise HTTPException(
            status_code=400,
            detail="Requisito do tipo 'acumulo' precisa de valor_minimo",
        )

    novo = PreRequisito(**pre_requisito.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[PreRequisitoResponse])
def listar_pre_requisitos(disciplina_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(PreRequisito)
    if disciplina_id is not None:
        query = query.filter(PreRequisito.disciplina_id == disciplina_id)
    return query.all()


@router.get("/{pre_requisito_id}", response_model=PreRequisitoResponse)
def buscar_pre_requisito(pre_requisito_id: int, db: Session = Depends(get_db)):
    pre_requisito = db.query(PreRequisito).filter(PreRequisito.id == pre_requisito_id).first()
    if not pre_requisito:
        raise HTTPException(status_code=404, detail="Pré-requisito não encontrado")
    return pre_requisito