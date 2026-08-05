from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Oferta(Base):
    __tablename__ = "oferta"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"), nullable=False)
    semestre = Column(String, nullable=False)  # ex: "2026.2"
    professor = Column(String, nullable=True)
    dia_semana = Column(String, nullable=False)  # "segunda", "terca", etc.
    horario_inicio = Column(Time, nullable=False)
    horario_fim = Column(Time, nullable=False)
    vagas = Column(Integer, nullable=True)

    disciplina = relationship("Disciplina", backref="ofertas")