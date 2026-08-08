from pydantic import BaseModel
from decimal import Decimal


class PreRequisitoBase(BaseModel):
    disciplina_id: int
    tipo: str  # "direto" ou "acumulo"
    disciplina_requisito_id: int | None = None
    natureza: str | None = None  # "pre_requisito", "co_requisito_direcional", "requisito_especial"
    valor_minimo: Decimal | None = None


class PreRequisitoCreate(PreRequisitoBase):
    pass


class PreRequisitoResponse(PreRequisitoBase):
    id: int

    class Config:
        from_attributes = True