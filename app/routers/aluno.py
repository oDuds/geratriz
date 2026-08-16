from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Header
from app.security import obter_aluno_id_do_token

from app.database import get_db
from app.models.aluno import Aluno
from app.schemas.aluno import AlunoCreate, AlunoResponse, LoginRequest, Token
from app.security import hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.post("/cadastro", response_model=AlunoResponse)
def cadastrar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    existente = db.query(Aluno).filter(Aluno.email == aluno.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_aluno = Aluno(
        nome=aluno.nome,
        email=aluno.email,
        senha_hash=hash_senha(aluno.senha),
        matriz_id=aluno.matriz_id,
    )
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno


@router.post("/login", response_model=Token)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.email == dados.email).first()

    if not aluno or not verificar_senha(dados.senha, aluno.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token({"sub": str(aluno.id)})
    return {"access_token": token, "token_type": "bearer"}



@router.get("/me", response_model=AlunoResponse)
def meus_dados(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não fornecido")

    token = authorization.replace("Bearer ", "")
    aluno_id = obter_aluno_id_do_token(token)

    if aluno_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return aluno