from pydantic import BaseModel, EmailStr


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    matriz_id: int


class AlunoResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    matriz_id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"