from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "chave-temporaria-trocar-depois")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hash)


def criar_token(dados: dict) -> str:
    dados_copia = dados.copy()
    expira_em = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copia.update({"exp": expira_em})
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)