from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AlunoDisciplina(Base):
    __tablename__ = "aluno_disciplina"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("aluno.id"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"), nullable=False)
    status = Column(String, nullable=False)  # "cursando", "aprovado", "reprovado", "pendente"

    aluno = relationship("Aluno", backref="historico")
    disciplina = relationship("Disciplina", backref="historico_alunos")