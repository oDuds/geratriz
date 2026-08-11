from sqlalchemy.orm import Session

from app.models.matriz import Matriz
from app.models.disciplina import Disciplina
from app.models.aluno_disciplina import AlunoDisciplina
from app.models.pre_requisito import PreRequisito
from app.models.aluno import Aluno


def calcular_carga_concluida(db: Session, aluno: Aluno) -> float:
    """Soma a carga (créditos ou horas) de tudo que o aluno já concluiu."""
    aprovados = (
        db.query(AlunoDisciplina)
        .filter(AlunoDisciplina.aluno_id == aluno.id, AlunoDisciplina.status == "aprovado")
        .all()
    )
    disciplina_ids = [a.disciplina_id for a in aprovados]
    if not disciplina_ids:
        return 0

    disciplinas = db.query(Disciplina).filter(Disciplina.id.in_(disciplina_ids)).all()
    return sum(d.carga for d in disciplinas)


def status_disciplina(db: Session, aluno_id: int, disciplina_id: int) -> str | None:
    """Retorna o status do aluno numa disciplina, ou None se nunca cursou."""
    registro = (
        db.query(AlunoDisciplina)
        .filter(
            AlunoDisciplina.aluno_id == aluno_id,
            AlunoDisciplina.disciplina_id == disciplina_id,
        )
        .first()
    )
    return registro.status if registro else None


def verificar_requisitos(db: Session, aluno: Aluno, disciplina: Disciplina) -> bool:
    """Verifica se o aluno cumpre TODOS os requisitos de uma disciplina."""
    requisitos = db.query(PreRequisito).filter(PreRequisito.disciplina_id == disciplina.id).all()

    if not requisitos:
        return True

    carga_concluida = calcular_carga_concluida(db, aluno)
    total_carga_matriz = aluno.matriz.total_carga

    for req in requisitos:
        if req.tipo == "direto":
            status = status_disciplina(db, aluno.id, req.disciplina_requisito_id)

            if req.natureza == "co_requisito_direcional":
                if status not in ("aprovado", "cursando"):
                    return False
            else:
                # pre_requisito ou requisito_especial (simplificado, tratado como pre_requisito)
                if status != "aprovado":
                    return False

        elif req.tipo == "acumulo":
            if total_carga_matriz == 0:
                return False
            percentual_ou_valor = (
                (carga_concluida / total_carga_matriz) * 100
                if aluno.matriz.unidade_carga == "creditos"
                else carga_concluida
            )
            if percentual_ou_valor < float(req.valor_minimo):
                return False

    return True


def periodo_atual_aluno(db: Session, aluno_id: int) -> int:
    """Estima o período atual do aluno: maior período sugerido entre as
    disciplinas já aprovadas, +1. Se não tem nada aprovado, considera 1."""
    aprovados = (
        db.query(AlunoDisciplina)
        .filter(AlunoDisciplina.aluno_id == aluno_id, AlunoDisciplina.status == "aprovado")
        .all()
    )
    disciplina_ids = [a.disciplina_id for a in aprovados]
    if not disciplina_ids:
        return 1

    disciplinas = db.query(Disciplina).filter(Disciplina.id.in_(disciplina_ids)).all()
    maior_periodo = max((d.periodo_sugerido for d in disciplinas), default=0)
    return maior_periodo + 1


def listar_disciplinas_elegiveis(db: Session, aluno_id: int, margem_periodos: int = 1) -> list[Disciplina]:
    """Fase 1: retorna disciplinas que o aluno pode cursar agora, priorizando
    o que faz sentido pro período atual dele (não pula pra frente à toa)."""
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        return []

    periodo_atual = periodo_atual_aluno(db, aluno_id)
    limite_periodo = periodo_atual + margem_periodos

    todas_disciplinas = (
        db.query(Disciplina)
        .filter(
            Disciplina.matriz_id == aluno.matriz_id,
            Disciplina.periodo_sugerido <= limite_periodo,
        )
        .all()
    )

    ja_aprovadas = {
        a.disciplina_id
        for a in db.query(AlunoDisciplina).filter(
            AlunoDisciplina.aluno_id == aluno_id, AlunoDisciplina.status == "aprovado"
        )
    }

    elegiveis = []
    for disciplina in todas_disciplinas:
        if disciplina.id in ja_aprovadas:
            continue
        if verificar_requisitos(db, aluno, disciplina):
            elegiveis.append(disciplina)

    return elegiveis