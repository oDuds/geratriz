from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.aluno_disciplina import AlunoDisciplina
from app.schemas.aluno_disciplina import AlunoDisciplinaCreate, AlunoDisciplinaResponse, AlunoDisciplinaLote
from app.security import exigir_aluno_logado

router = APIRouter(prefix="/aluno-disciplinas", tags=["Histórico do Aluno"])


from app.security import exigir_aluno_logado


@router.post("/", response_model=AlunoDisciplinaResponse)
def registrar_status(
    item: AlunoDisciplinaCreate,
    db: Session = Depends(get_db),
    aluno_id_logado: int = Depends(exigir_aluno_logado),
):
    if item.aluno_id != aluno_id_logado:
        raise HTTPException(status_code=403, detail="Não é possível alterar histórico de outro aluno")

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
def listar_historico(db: Session = Depends(get_db), aluno_id_logado: int = Depends(exigir_aluno_logado)):
    return db.query(AlunoDisciplina).filter(AlunoDisciplina.aluno_id == aluno_id_logado).all()


@router.post("/lote", response_model=list[AlunoDisciplinaResponse])
def registrar_status_em_lote(
    dados: AlunoDisciplinaLote,
    db: Session = Depends(get_db),
    aluno_id_logado: int = Depends(exigir_aluno_logado),
):
    for item in dados.itens:
        if item.aluno_id != aluno_id_logado:
            raise HTTPException(status_code=403, detail="Não é possível alterar histórico de outro aluno")

    resultados = []
    for item in dados.itens:
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
            resultados.append(existente)
        else:
            novo = AlunoDisciplina(**item.model_dump())
            db.add(novo)
            resultados.append(novo)

    db.commit()
    for r in resultados:
        db.refresh(r)

    return resultados