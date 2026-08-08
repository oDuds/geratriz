from pydantic import BaseModel
from datetime import time


class OfertaBase(BaseModel):
    disciplina_id: int
    semestre: str
    professor: str | None = None
    dia_semana: str
    horario_inicio: time
    horario_fim: time
    vagas: int | None = None


class OfertaCreate(OfertaBase):
    pass


class OfertaResponse(OfertaBase):
    id: int

    class Config:
        from_attributes = True