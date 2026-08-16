from pydantic import BaseModel


class AlunoDisciplinaBase(BaseModel):
    aluno_id: int
    disciplina_id: int
    status: str  # "cursando", "aprovado", "reprovado", "pendente"


class AlunoDisciplinaCreate(AlunoDisciplinaBase):
    pass


class AlunoDisciplinaResponse(AlunoDisciplinaBase):
    id: int

    class Config:
        from_attributes = True

class AlunoDisciplinaLote(BaseModel):
    itens: list[AlunoDisciplinaBase]