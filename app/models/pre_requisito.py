from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class PreRequisito(Base):
    __tablename__ = "pre_requisito"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"), nullable=False)
    tipo = Column(String, nullable=False)  # "direto" ou "acumulo"

    disciplina_requisito_id = Column(Integer, ForeignKey("disciplina.id"), nullable=True)
    natureza = Column(String, nullable=True)  # "pre_requisito", "co_requisito_direcional", "requisito_especial"

    valor_minimo = Column(Numeric, nullable=True)  # percentual de creditos(2018) ou horas relogios absolutas (2023)

    disciplina = relationship("Disciplina", foreign_keys=[disciplina_id], backref="requisitos")
    disciplina_requisito = relationship("Disciplina", foreign_keys=[disciplina_requisito_id])