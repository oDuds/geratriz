from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Aluno(Base):
    __tablename__ = "aluno"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    matriz_id = Column(Integer, ForeignKey("matriz.id"), nullable=False)

    matriz = relationship("Matriz", backref="alunos")