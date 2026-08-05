from pydantic import BaseModel


class MatrizBase(BaseModel):
    nome: str
    unidade_carga: str
    total_carga: int


class MatrizCreate(MatrizBase):
    pass


class MatrizResponse(MatrizBase):
    id: int

    class Config:
        from_attributes = True