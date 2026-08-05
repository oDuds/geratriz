from sqlalchemy import Column, Integer, String
from app.database import Base


class Matriz(Base):
    __tablename__ = "matriz"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    unidade_carga = Column(String, nullable=False)
    total_carga = Column(Integer, nullable=False)