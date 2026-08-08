from pydantic import BaseModel
from datetime import time


class OfertaBase(BaseModel):
    disciplina_id: int
    semestre: str
    professor: str | None = None
    dia_semana: str | None = None
    horario_inicio: time | None = None
    horario_fim: time | None = None
    vagas: int | None = None


class OfertaCreate(OfertaBase):
    pass


class OfertaResponse(OfertaBase):
    id: int

    class Config:
        from_attributes = True