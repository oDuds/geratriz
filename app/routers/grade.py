from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.otimizador import montar_grade
from app.schemas.grade import GradeResponse, OfertaNaGrade
from app.security import obter_aluno_id_do_token

router = APIRouter(prefix="/grade", tags=["Grade"])


@router.get("/gerar", response_model=GradeResponse)
def gerar_grade(
    semestre: str,
    max_creditos: int | None = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não fornecido")

    token = authorization.replace("Bearer ", "")
    aluno_id = obter_aluno_id_do_token(token)

    if aluno_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    resultado = montar_grade(db, aluno_id=aluno_id, semestre=semestre, max_creditos=max_creditos)

    ofertas_formatadas = [
        OfertaNaGrade(
            disciplina_codigo=o.disciplina.codigo,
            disciplina_nome=o.disciplina.nome,
            dia_semana=o.dia_semana,
            horario_inicio=o.horario_inicio,
            horario_fim=o.horario_fim,
        )
        for o in resultado["grade"]
    ]

    return GradeResponse(
        total_disciplinas=resultado["total_disciplinas"],
        total_creditos=resultado["total_creditos"],
        grade=ofertas_formatadas,
    )