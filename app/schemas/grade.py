from pydantic import BaseModel
from datetime import time


class OfertaNaGrade(BaseModel):
    disciplina_codigo: str
    disciplina_nome: str
    dia_semana: str | None
    horario_inicio: time | None
    horario_fim: time | None

    class Config:
        from_attributes = True


class GradeResponse(BaseModel):
    total_disciplinas: int
    total_creditos: float
    grade: list[OfertaNaGrade]