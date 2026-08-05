from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Disciplina(Base):
    __tablename__ = "disciplina"

    id = Column(Integer, primary_key=True, index=True)
    matriz_id = Column(Integer, ForeignKey("matriz.id"), nullable=False)
    codigo = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    periodo_sugerido = Column(Integer, nullable=False)
    carga = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)

    matriz = relationship("Matriz", backref="disciplinas")