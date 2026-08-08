from pydantic import BaseModel


class DisciplinaBase(BaseModel):
    matriz_id: int
    codigo: str
    nome: str
    periodo_sugerido: int
    carga: int
    tipo: str


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaResponse(DisciplinaBase):
    id: int

    class Config:
        from_attributes = True