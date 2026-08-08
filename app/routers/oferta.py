from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.oferta import Oferta
from app.schemas.oferta import OfertaCreate, OfertaResponse

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])


@router.post("/", response_model=OfertaResponse)
def criar_oferta(oferta: OfertaCreate, db: Session = Depends(get_db)):
    nova_oferta = Oferta(**oferta.model_dump())
    db.add(nova_oferta)
    db.commit()
    db.refresh(nova_oferta)
    return nova_oferta


@router.get("/", response_model=list[OfertaResponse])
def listar_ofertas(
    disciplina_id: int | None = None,
    semestre: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Oferta)
    if disciplina_id is not None:
        query = query.filter(Oferta.disciplina_id == disciplina_id)
    if semestre is not None:
        query = query.filter(Oferta.semestre == semestre)
    return query.all()


@router.get("/{oferta_id}", response_model=OfertaResponse)
def buscar_oferta(oferta_id: int, db: Session = Depends(get_db)):
    oferta = db.query(Oferta).filter(Oferta.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")
    return oferta